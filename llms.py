# import os
# import threading
# import logging
# from llama_cpp import Llama
# from config import MODEL_PATHS, MODEL_PARAMS

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__) # for logging info

# class LLMManager:
#     _instance = None
#     _lock = threading.Lock()
#     _models = {}

#     def __new__(cls):  #ensure there can ony be one instance (don't want multiple model states and stuff)
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._models = {}
#         return cls._instance


#     def load_model(self, model_name: str):
#         if model_name not in self._models: # loads model if not already loaded / in models
#             model_path = MODEL_PATHS[model_name]
#             params = MODEL_PARAMS[model_name]

#             logger.info(f"Loading model {model_name} from {model_path}")
#             print(f"Model path: {model_path}")

#             if not os.path.exists(model_path):
#                 logger.error(f"Model file not found at {model_path}")
#                 raise FileNotFoundError(f"Model file not found at {model_path}")

#             try:
#                 model = Llama(model_path=model_path, **params)
#                 self._models[model_name] = model
#                 logger.info(f"Successfully loaded {model_name}")
#                 return model
            



#             except Exception as e:
#                 logger.error(f"Error loading model: {str(e)}")
#                 raise

#         return self._models[model_name] # loads model bc already loaded



#     # generates the message / response based on inputs
#     def generate(self, model_name: str, prompt: str, max_tokens: int = 512, temperature: float = 0.0):
#         model = self.load_model(model_name) # loads inputted model


#         try: # tries to generate a response based on arguments and model//errors if doesn't succeed
#             output = model.create_completion(
#                 prompt=prompt,
#                 max_tokens=max_tokens,
#                 temperature=temperature,
#                 stop=["</s>", "\n\n"]
#             )
#             return output['choices'][0]['text'] # returns response if successful
        
#         except Exception as e:
#             logger.error(f"Generation error: {str(e)}")
#             raise
import os
import threading
import logging
from llama_cpp import Llama
from config import MODEL_PATHS, MODEL_PARAMS
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMManager:
    _instance: Optional['LLMManager'] = None
    _lock = threading.Lock()
    _models: Dict[str, Llama] = {}
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:  # Thread safety for initialization
                if cls._instance is None:  # Double-check pattern
                    cls._instance = super().__new__(cls)
                    cls._instance._models = {}
        return cls._instance
    
    def load_model(self, model_name: str) -> Llama:
        """Load model if not already loaded, otherwise return cached model."""
        with self._lock:  # Thread safety for model loading
            if model_name not in self._models:
                model_path = MODEL_PATHS[model_name]
                params = MODEL_PARAMS[model_name]
                
                logger.info(f"Loading model {model_name} from {model_path}")
                
                if not os.path.exists(model_path):
                    logger.error(f"Model file not found at {model_path}")
                    raise FileNotFoundError(f"Model file not found at {model_path}")
                
                try:
                    # Add n_ctx if not in params to control context window
                    if 'n_ctx' not in params:
                        params['n_ctx'] = 1024  # or whatever size you prefer
                        
                    # Add n_batch if not in params to control batch size
                    if 'n_batch' not in params:
                        params['n_batch'] = 256  # adjust based on your GPU/CPU
                        
                    model = Llama(model_path=model_path, **params)
                    self._models[model_name] = model
                    logger.info(f"Successfully loaded {model_name}")
                    
                except Exception as e:
                    logger.error(f"Error loading model: {str(e)}")
                    raise
                
            return self._models[model_name]
    

    def generate_stream(self, model_name: str, prompt: str, max_tokens: int = 256, temperature: float = 0.0):
        """Generate streaming completion."""
        try:
            model = self.load_model(model_name)
            
            for output in model.create_completion(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                frequency_penalty=2.0,
                
                presence_penalty=1.8,
                stop=["</s>", "\n\n", "***", "```"],
                stream=True
            ):
                if output and 'choices' in output and len(output['choices']) > 0: # blank
                    text = output['choices'][0]['text']
                    text = text.replace('*', '').replace('%', '')
                    if text:
                        yield text
                        
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            raise

    
    
    
    def generate(self, model_name: str, prompt: str, max_tokens: int = 256, temperature: float = 0.0) -> str:
        """Generate completion using cached model."""
        try:
            model = self.load_model(model_name) 
            
            output = model.create_completion(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                frequency_penalty=2.0,
                stop=["</s>", "\n\n"]
            )
            
            response = output['choices'][0]['text']
            return response.strip()  
            
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            raise
    
    def unload_model(self, model_name: str) -> None:
        """Explicitly unload a model to free memory."""
        with self._lock:
            if model_name in self._models:
                del self._models[model_name]
                logger.info(f"Unloaded model {model_name}")
