### Optimizing Vending Machine Inventory with AI: A Deep Dive into Model Selection
#### Introduction:
Vending machines, once simple dispensers, are evolving into data-driven hubs. To maximize customer satisfaction and revenue, owners need real-time insights into product consumption. This article explores how Vision AI can enhance inventory management by using cameras to monitor purchases.

#### The Challenge:
Traditional inventory methods often rely on manual checks or unreliable sensors. Vision AI offers a more accurate and efficient solution. However, the diversity of products in vending machines, coupled with varying package sizes and shapes, presents a unique challenge.

#### The Solution: Deep Learning
Deep learning, a subset of AI, is ideally suited for this task. It can learn complex patterns from vast datasets, making it capable of identifying and classifying products even in the face of variations.

#### Beyond the model: The Vision AI stack
While the AI model is crucial, it is part of the larger vision AI solution stack. Key components include:

#### Hardware Selection: Choosing the right camera with desired FoV that can capture high quality images in various lighting conditions
1. Hardware Installation: Ensuring cameras are securely mounted and positioned to capture optimal product views without being intrusive or compromising customer experience.
2. Data Transmission: Selecting reliable communication mechanism to transmit image/video data to the processing system
3. Processing System: Determining whether to run the AI model on-device (edge computing) or in the cloud or in a hybrid fashion.
4. Data Storage: Saving necessary data to support future analysis and reporting
5. Data Presentation: Helping owners visualize the insights via a front-end application

#### AI Model Development
To accurately track product purchases, we need a reference database containing images and corresponding information for each product in the vending machine, including product name and location within the machine. Our motion-detection camera captures footage whenever a customer makes a purchase. By analyzing the movement of the product from its slot, we can effectively identify the specific item purchased.

First Choice: Multimodal Large Language Model
A promising approach is to leverage a Multimodal Large Language Model (MLLM) to identify products in the image. MLLMs, trained on vast amounts of text and image data, possess advanced capabilities in understanding and processing both visual and textual information. Hence, there is a high chance that it can perform zero-shot detection of product packages in images. In addition, it is easy to invoke these models by only providing a detailed prompt through an API call. If this works, it would eliminate the need for complex, custom-built models, simplifying the development process.

In addition, we expect the model to return the names of all the packaged products in the image and their location in the form of bounding box.

There are 2 types of tasks we want the LMM to be good at:
1. Visual reasoning based on text in images - TextVQA is the standard benchmark to measure a model's performance in this regard
2. Visual search to localize key objects in the image.

Below is the list of top MLLMs available today. 
1. Gemini 1.5 Pro: https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf
2. GPT4o: https://openai.com/index/gpt-4-research/
3. Claude3: https://www.anthropic.com/news/claude-3-family, https://docs.anthropic.com/en/docs/build-with-claude/vision
4. Grok-1.5v: https://x.ai/blog/grok-1.5v
5. Llamma3-V 405B: https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/, https://scontent-sjc3-1.xx.fbcdn.net/v/t39.2365-6/453304228_1160109801904614_7143520450792086005_n.pdf
6. NVLM1.0: https://research.nvidia.com/labs/adlr/NVLM-1/

We will evaluate the top 3 models from the above list that have the best vision capabilities. Subsequently, we will also evaluate some domain-specific vision models that use the latest transformer architecture and also one that use CNN and R-CNN architectures.
