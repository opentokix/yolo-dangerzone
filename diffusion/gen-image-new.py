#!/usr/bin/env python3
import click
import torch
from diffusers import StableDiffusionPipeline
from datetime import datetime
import os


def check_device():
    """Check if MPS (Metal Performance Shaders) is available."""
    if torch.backends.mps.is_available():
        print("MPS is available")
        return "mps"
    elif torch.cuda.is_available():
        print("CUDA is available")
        return "cuda"
    return "cpu"


def get_pipeline(model_id="):
    """Initialize the Stable Diffusion pipeline."""
    device = check_device()

    # Initialize pipeline with Apple Silicon optimizations
    pipeline = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16
    )

    if device == "mps":
        pipeline = pipeline.to(device)
        # Enable memory efficient attention if needed
        pipeline.enable_attention_slicing()

    return pipeline


def generate_filename():
    """Generate a filename with current date and time."""
    now = datetime.now()
    return f"generated-{now.strftime('%Y%m%d-%H%M%S')}.png"


@click.command()
@click.option('--prompt', required=True, help='The prompt for image generation')
@click.option('--model', default="runwayml/stable-diffusion-v1-5",
              help='Hugging Face model ID (default: stable-diffusion-v1-5)')
@click.option('--output-dir', default="generated",
              help='Output directory for generated images')
def generate(prompt, model, output_dir):
    """Generate an image using Stable Diffusion on Apple Silicon."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Initialize pipeline
        print(f"Initializing Stable Diffusion with model: {model}")
        pipeline = get_pipeline(model)

        # Generate image
        print(f"Generating image for prompt: {prompt}")
        image = pipeline(
            prompt,
            num_inference_steps=50,
            guidance_scale=7.5
        ).images[0]

        # Save image
        filename = os.path.join(output_dir, generate_filename())
        image.save(filename)
        print(f"Image saved as: {filename}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    generate()
