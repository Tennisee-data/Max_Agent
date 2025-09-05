# summariser.py
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# import torch  # Unused direct import

# import intel_extension_for_pytorch as ipex
import time


class Summariser:
    def __init__(self, model_id, device=-1):
        self.model_id = model_id
        self.device = device
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.load_model()

    def load_model(self):
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

        try:
            logging.info(f"Loading tokenizer for model '{self.model_id}'...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            logging.info(f"Loading model '{self.model_id}'...")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_id)
            # logging.info("Optimising model with Intel® Extension for PyTorch...")
            # self.model = ipex.optimize(self.model, dtype=torch.float32)
            logging.info("Creating summarisation pipeline...")
            self.pipeline = pipeline(
                "summarization",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
            )
            logging.info("Model and pipeline loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load model '{self.model_id}': {e}")
            raise

    def count_tokens(self, text):
        tokens = self.tokenizer(text, return_tensors="pt", truncation=False)
        return tokens.input_ids.shape[1]

    def summarise_chunk(self, chunk, min_ratio, max_ratio, retries=3, delay=3):
        chunk_length = self.count_tokens(chunk)
        dynamic_min_length = max(int(chunk_length * min_ratio), 1)
        dynamic_max_length = max(int(chunk_length * max_ratio), dynamic_min_length + 1)

        logging.info(
            f"Summarising chunk with {chunk_length} tokens "
            f"(min: {dynamic_min_length}, max: {dynamic_max_length})"
        )
        for attempt in range(retries):
            try:
                summary = self.pipeline(
                    chunk,
                    max_length=dynamic_max_length,
                    min_length=dynamic_min_length,
                    do_sample=False,
                )[0]["summary_text"]
                logging.info("Chunk summarised successfully.")
                return summary
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} - Error summarizing chunk: {e}")
                if attempt < retries - 1:
                    logging.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logging.error("Max retries reached. Skipping this chunk.")
                    return ""

    def summarise_chunks_parallel(
        self, chunks, min_ratio=0.20, max_ratio=0.35, max_workers=None
    ):
        if max_workers is None:
            max_workers = os.cpu_count() or 4

        partial_summaries = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.summarise_chunk, chunk, min_ratio, max_ratio)
                for chunk in chunks
            ]
            for future in as_completed(futures):
                summary = future.result()
                if summary:
                    partial_summaries.append(summary)
        return partial_summaries

    def summarise(
        self,
        chunks,
        first_min_ratio,
        first_max_ratio,
        second_min_ratio,
        second_max_ratio,
    ):
        # First summarisation tier
        logging.info("Starting first summarisation tier...")
        partial_summaries = self.summarise_chunks_parallel(
            chunks, min_ratio=first_min_ratio, max_ratio=first_max_ratio
        )

        combined_summary = " ".join(partial_summaries)
        combined_length = self.count_tokens(combined_summary)
        logging.info(f"Combined summaries token length: {combined_length}")

        # Check if combined summary exceeds model's max length
        if combined_length > self.tokenizer.model_max_length:
            logging.warning(
                f"Combined summary exceeds model's max length "
                f"({self.tokenizer.model_max_length} tokens). "
                f"Performing second summarization tier..."
            )
            dynamic_min_length = max(int(combined_length * second_min_ratio), 1)
            dynamic_max_length = max(
                int(combined_length * second_max_ratio), dynamic_min_length + 1
            )

            try:
                final_summary = self.pipeline(
                    combined_summary,
                    max_length=dynamic_max_length,
                    min_length=dynamic_min_length,
                    do_sample=False,
                )[0]["summary_text"]
                logging.info("Final summary generated successfully.")
                return final_summary
            except Exception as e:
                logging.error(f"Error in second summarisation tier: {e}")
                return "Summary could not be generated."
        else:
            logging.info(
                "Combined summary within token limits. Returning combined summary."
            )
            return combined_summary
