# SPDX-License-Identifier: Apache-2.0

from vllm import LLM, SamplingParams

# Sample prompts.
# prompts = [
#     "Hello, my name is",
#     "The president of the United States is",
#     "The capital of France is",
#     "The future of AI is",
# ]

# prompts = [
#     "ai infra is"
# ]

i = 10
prompts = [f"AI is {i}" for i in range(i)]

# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)


def main():
    # Create an LLM.

    # COMMENT(Jeremy: 2025-04-22 ): 在生成llm时已经生成了IIm_engine; llm_engine中已经生成了tokenizer, processor,output_processor, engine_core;engine_core中会开启EngineCore幕后进程, 只是在等待接收请求

    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v0.6")
    # Generate texts from the prompts.
    # The output is a list of RequestOutput objects
    # that contain the prompt, generated text, and other information.
    outputs = llm.generate(prompts, sampling_params)
    # Print the outputs.
    print("\nGenerated Outputs:\n" + "-" * 60)
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt:    {prompt!r}")
        print(f"Output:    {generated_text!r}")
        print("-" * 60)


if __name__ == "__main__":
    main()
