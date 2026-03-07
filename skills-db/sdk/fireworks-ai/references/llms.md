# Fireworks AI Docs

## Docs

- [Exporting Billing Metrics](https://docs.fireworks.ai/accounts/exporting-billing-metrics.md): Export billing and usage metrics for all Fireworks services
- [Service Accounts](https://docs.fireworks.ai/accounts/service-accounts.md): How to manage and use service accounts in Fireworks
- [Custom SSO](https://docs.fireworks.ai/accounts/sso.md): Set up custom Single Sign-On (SSO) authentication for Fireworks AI
- [Managing users](https://docs.fireworks.ai/accounts/users.md): Add, delete, and manage roles for users in your Fireworks account
- [Streaming Transcription](https://docs.fireworks.ai/api-reference/audio-streaming-transcriptions.md)
- [Transcribe audio](https://docs.fireworks.ai/api-reference/audio-transcriptions.md)
- [Translate audio](https://docs.fireworks.ai/api-reference/audio-translations.md)
- [Cancel Reinforcement Fine-tuning Job](https://docs.fireworks.ai/api-reference/cancel-reinforcement-fine-tuning-job.md)
- [Create API Key](https://docs.fireworks.ai/api-reference/create-api-key.md)
- [Create Batch Inference Job](https://docs.fireworks.ai/api-reference/create-batch-inference-job.md)
- [Create Batch Request](https://docs.fireworks.ai/api-reference/create-batch-request.md)
- [Create Dataset](https://docs.fireworks.ai/api-reference/create-dataset.md)
- [Load LoRA](https://docs.fireworks.ai/api-reference/create-deployed-model.md)
- [Create Deployment](https://docs.fireworks.ai/api-reference/create-deployment.md)
- [null](https://docs.fireworks.ai/api-reference/create-dpo-job.md)
- [Create Evaluation Job](https://docs.fireworks.ai/api-reference/create-evaluation-job.md)
- [Create Evaluator](https://docs.fireworks.ai/api-reference/create-evaluator.md): Creates a custom evaluator for scoring model outputs. Evaluators use the
[Eval Protocol](https://evalprotocol.io) to define test cases, run model
inference, and score responses. They are used with evaluation jobs and
Reinforcement Fine-Tuning (RFT).

## Source Code Requirements

Your project should contain:
- `requirements.txt` - Python dependencies for your evaluator
- `test_*.py` - Pytest test file(s) with
  [`@evaluation_test`](https://evalprotocol.io/reference/evaluation-test)
  decorated functions
- Any additional code/modules your evaluator needs

## Workflow

**Recommended:** Use the [`ep upload`](https://evalprotocol.io/reference/cli#ep-upload)
CLI command to handle all these steps automatically.

If using the API directly:

1. Call this endpoint to create the evaluator resource
2. Package your source directory as a `.tar.gz` (respecting `.gitignore`)
3. Call [Get Evaluator Upload Endpoint](/api-reference/get-evaluator-upload-endpoint) to get a signed upload URL
4. `PUT` the tar.gz file to the signed URL
5. Call [Validate Evaluator Upload](/api-reference/validate-evaluator-upload) to trigger server-side validation
6. Poll [Get Evaluator](/api-reference/get-evaluator) until ready

Once active, reference the evaluator in [Create Evaluation Job](/api-reference/create-evaluation-job) or [Create Reinforcement Fine-tuning Job](/api-reference/create-reinforcement-fine-tuning-job).
- [Create Model](https://docs.fireworks.ai/api-reference/create-model.md)
- [Create Reinforcement Fine-tuning Job](https://docs.fireworks.ai/api-reference/create-reinforcement-fine-tuning-job.md)
- [Create Reinforcement Fine-tuning Step](https://docs.fireworks.ai/api-reference/create-reinforcement-fine-tuning-step.md)
- [null](https://docs.fireworks.ai/api-reference/create-secret.md)
- [Create Supervised Fine-tuning Job](https://docs.fireworks.ai/api-reference/create-supervised-fine-tuning-job.md)
- [Create User](https://docs.fireworks.ai/api-reference/create-user.md)
- [Create embeddings](https://docs.fireworks.ai/api-reference/creates-an-embedding-vector-representing-the-input-text.md)
- [Delete API Key](https://docs.fireworks.ai/api-reference/delete-api-key.md)
- [Delete Batch Inference Job](https://docs.fireworks.ai/api-reference/delete-batch-inference-job.md)
- [Delete Dataset](https://docs.fireworks.ai/api-reference/delete-dataset.md)
- [Unload LoRA](https://docs.fireworks.ai/api-reference/delete-deployed-model.md)
- [Delete Deployment](https://docs.fireworks.ai/api-reference/delete-deployment.md)
- [null](https://docs.fireworks.ai/api-reference/delete-dpo-job.md)
- [Delete Evaluation Job](https://docs.fireworks.ai/api-reference/delete-evaluation-job.md)
- [Delete Evaluator](https://docs.fireworks.ai/api-reference/delete-evaluator.md): Deletes an evaluator and its associated versions and build artifacts.
- [Delete Model](https://docs.fireworks.ai/api-reference/delete-model.md)
- [Delete Reinforcement Fine-tuning Job](https://docs.fireworks.ai/api-reference/delete-reinforcement-fine-tuning-job.md)
- [Delete Reinforcement Fine-tuning Step](https://docs.fireworks.ai/api-reference/delete-reinforcement-fine-tuning-step.md)
- [Delete Response](https://docs.fireworks.ai/api-reference/delete-response.md): Deletes a model response by its ID. Once deleted, the response data will be gone immediately and permanently.

The response cannot be recovered and any conversations that reference this response ID will no longer be able to access it.
- [null](https://docs.fireworks.ai/api-reference/delete-secret.md)
- [Delete Supervised Fine-tuning Job](https://docs.fireworks.ai/api-reference/delete-supervised-fine-tuning-job.md)
- [Execute one training step for keep-alive Reinforcement Fine-tuning Step](https://docs.fireworks.ai/api-reference/execute-reinforcement-fine-tuning-step.md)
- [Generate an image with FLUX.1 [schnell] FP8](https://docs.fireworks.ai/api-reference/generate-a-new-image-from-a-text-prompt.md)
- [Generate or edit an image with FLUX.1 Kontext](https://docs.fireworks.ai/api-reference/generate-or-edit-image-using-flux-kontext.md)
- [Get Account](https://docs.fireworks.ai/api-reference/get-account.md)
- [Get Batch Inference Job](https://docs.fireworks.ai/api-reference/get-batch-inference-job.md)
- [Check Batch Status](https://docs.fireworks.ai/api-reference/get-batch-status.md)
- [Get Dataset](https://docs.fireworks.ai/api-reference/get-dataset.md)
- [Get Dataset Download Endpoint](https://docs.fireworks.ai/api-reference/get-dataset-download-endpoint.md)
- [Get Dataset Upload Endpoint](https://docs.fireworks.ai/api-reference/get-dataset-upload-endpoint.md)
- [Get LoRA](https://docs.fireworks.ai/api-reference/get-deployed-model.md)
- [Get Deployment](https://docs.fireworks.ai/api-reference/get-deployment.md)
- [Get Deployment Shape](https://docs.fireworks.ai/api-reference/get-deployment-shape.md)
- [Get Deployment Shape Version](https://docs.fireworks.ai/api-reference/get-deployment-shape-version.md)
- [null](https://docs.fireworks.ai/api-reference/get-dpo-job.md)
- [null](https://docs.fireworks.ai/api-reference/get-dpo-job-metrics-file-endpoint.md)
- [Get Evaluation Job](https://docs.fireworks.ai/api-reference/get-evaluation-job.md)
- [Get Evaluation Job execution logs (stream log endpoint + tracing IDs).](https://docs.fireworks.ai/api-reference/get-evaluation-job-log-endpoint.md)
- [Get Evaluator](https://docs.fireworks.ai/api-reference/get-evaluator.md): Retrieves an evaluator by name. Use this to monitor build progress after
creation (**step 6** in the [Create Evaluator](/api-reference/create-evaluator) workflow).

Possible states:

- `BUILDING` - Environment is being prepared
- `ACTIVE` - Evaluator is ready to use
- `BUILD_FAILED` - Check build logs via [Get Evaluator Build Log Endpoint](/api-reference/get-evaluator-build-log-endpoint)
- [Get Evaluator Build Log Endpoint](https://docs.fireworks.ai/api-reference/get-evaluator-build-log-endpoint.md): Returns a signed URL to download the evaluator's build logs. Useful for
debugging `BUILD_FAILED` state.
- [Get Evaluator Source Code Endpoint](https://docs.fireworks.ai/api-reference/get-evaluator-source-code-endpoint.md): Returns a signed URL to download the evaluator's source code archive.
Useful for debugging or reviewing the uploaded code.
- [Get Evaluator Upload Endpoint](https://docs.fireworks.ai/api-reference/get-evaluator-upload-endpoint.md): Returns signed URLs for uploading evaluator source code (**step 3** in the
[Create Evaluator](/api-reference/create-evaluator) workflow). After receiving
the signed URL, upload your `.tar.gz` archive using HTTP `PUT` with
`Content-Type: application/octet-stream` header.
- [Get generated image from FLUX.1 Kontext](https://docs.fireworks.ai/api-reference/get-generated-image-from-flux-kontex.md)
- [Get Model](https://docs.fireworks.ai/api-reference/get-model.md)
- [Get Model Download Endpoint](https://docs.fireworks.ai/api-reference/get-model-download-endpoint.md)
- [Get Model Upload Endpoint](https://docs.fireworks.ai/api-reference/get-model-upload-endpoint.md)
- [Get Reinforcement Fine-tuning Job](https://docs.fireworks.ai/api-reference/get-reinforcement-fine-tuning-job.md)
- [Get Reinforcement Fine-tuning Step](https://docs.fireworks.ai/api-reference/get-reinforcement-fine-tuning-step.md)
- [Get Response](https://docs.fireworks.ai/api-reference/get-response.md)
- [Get Secret](https://docs.fireworks.ai/api-reference/get-secret.md): Retrieves a secret by name. Note that the `value` field is not returned in the response for security reasons. Only the `name` and `key_name` fields are included.
- [Get Supervised Fine-tuning Job](https://docs.fireworks.ai/api-reference/get-supervised-fine-tuning-job.md)
- [Get User](https://docs.fireworks.ai/api-reference/get-user.md)
- [Introduction](https://docs.fireworks.ai/api-reference/introduction.md)
- [List Accounts](https://docs.fireworks.ai/api-reference/list-accounts.md)
- [List API Keys](https://docs.fireworks.ai/api-reference/list-api-keys.md)
- [List Batch Inference Jobs](https://docs.fireworks.ai/api-reference/list-batch-inference-jobs.md)
- [List Datasets](https://docs.fireworks.ai/api-reference/list-datasets.md)
- [List LoRAs](https://docs.fireworks.ai/api-reference/list-deployed-models.md)
- [List Deployment Shapes Versions](https://docs.fireworks.ai/api-reference/list-deployment-shape-versions.md)
- [List Deployment Shapes](https://docs.fireworks.ai/api-reference/list-deployment-shapes.md)
- [List Deployments](https://docs.fireworks.ai/api-reference/list-deployments.md)
- [null](https://docs.fireworks.ai/api-reference/list-dpo-jobs.md)
- [List Evaluation Jobs](https://docs.fireworks.ai/api-reference/list-evaluation-jobs.md)
- [List Evaluators](https://docs.fireworks.ai/api-reference/list-evaluators.md): Lists all evaluators for an account with pagination support.
- [List Models](https://docs.fireworks.ai/api-reference/list-models.md)
- [List Reinforcement Fine-tuning Jobs](https://docs.fireworks.ai/api-reference/list-reinforcement-fine-tuning-jobs.md)
- [List Reinforcement Fine-tuning Steps](https://docs.fireworks.ai/api-reference/list-reinforcement-fine-tuning-steps.md)
- [List Responses](https://docs.fireworks.ai/api-reference/list-responses.md): Get a list of all responses for the authenticated account.

Args:
    limit: Maximum number of responses to return (default: 20, max: 100)
    after: Cursor for pagination - return responses after this ID
    before: Cursor for pagination - return responses before this ID
- [List Secrets](https://docs.fireworks.ai/api-reference/list-secrets.md): Lists all secrets for an account. Note that the `value` field is not returned in the response for security reasons. Only the `name` and `key_name` fields are included for each secret.
- [List Supervised Fine-tuning Jobs](https://docs.fireworks.ai/api-reference/list-supervised-fine-tuning-jobs.md)
- [List Users](https://docs.fireworks.ai/api-reference/list-users.md)
- [Create Chat Completion](https://docs.fireworks.ai/api-reference/post-chatcompletions.md): Create a completion for the provided prompt and parameters.
- [Create Completion](https://docs.fireworks.ai/api-reference/post-completions.md): Create a completion for the provided prompt and parameters.
- [Create Response](https://docs.fireworks.ai/api-reference/post-responses.md): Creates a model response, optionally interacting with custom tools via the Model Context Protocol (MCP). This endpoint supports conversational continuation and streaming.

Explore our cookbooks for detailed examples:

- [Basic MCP Usage](https://github.com/fw-ai/cookbook/blob/main/learn/response-api/fireworks_mcp_examples.ipynb)
- [Streaming with MCP](https://github.com/fw-ai/cookbook/blob/main/learn/response-api/fireworks_mcp_with_streaming.ipynb)
- [Conversational History with `previous_response_id`](https://github.com/fw-ai/cookbook/blob/main/learn/response-api/fireworks_previous_response_cookbook.ipynb)
- [Basic Streaming](https://github.com/fw-ai/cookbook/blob/main/learn/response-api/fireworks_streaming_example.ipynb)
- [Controlling Response Storage](https://github.com/fw-ai/cookbook/blob/main/learn/response-api/mcp_server_with_store_false_argument.ipynb)
- [Prepare Model for different precisions](https://docs.fireworks.ai/api-reference/prepare-model.md)
- [Rerank documents](https://docs.fireworks.ai/api-reference/rerank-documents.md): Rerank documents for a query using relevance scoring
- [Resume Dpo Job](https://docs.fireworks.ai/api-reference/resume-dpo-job.md)
- [Resume Reinforcement Fine-tuning Job](https://docs.fireworks.ai/api-reference/resume-reinforcement-fine-tuning-job.md)
- [Resume Rlor Trainer Job](https://docs.fireworks.ai/api-reference/resume-reinforcement-fine-tuning-step.md)
- [Resume Supervised Fine-tuning Job](https://docs.fireworks.ai/api-reference/resume-supervised-fine-tuning-job.md)
- [Scale Deployment to a specific number of replicas or to zero](https://docs.fireworks.ai/api-reference/scale-deployment.md)
- [Undelete Deployment](https://docs.fireworks.ai/api-reference/undelete-deployment.md)
- [Update Dataset](https://docs.fireworks.ai/api-reference/update-dataset.md)
- [Update LoRA](https://docs.fireworks.ai/api-reference/update-deployed-model.md)
- [Update Deployment](https://docs.fireworks.ai/api-reference/update-deployment.md)
- [Update Evaluator](https://docs.fireworks.ai/api-reference/update-evaluator.md): Updates evaluator metadata (display_name, description, default_dataset).
Changing `requirements` or `entry_point` triggers a rebuild. To upload new
source code, set `prepare_code_upload: true` then follow the upload flow.
- [Update Model](https://docs.fireworks.ai/api-reference/update-model.md)
- [null](https://docs.fireworks.ai/api-reference/update-secret.md)
- [Update User](https://docs.fireworks.ai/api-reference/update-user.md)
- [Upload Dataset Files](https://docs.fireworks.ai/api-reference/upload-dataset-files.md): Provides a streamlined way to upload a dataset file in a single API request. This path can handle file sizes up to 150Mb. For larger file sizes use [Get Dataset Upload Endpoint](get-dataset-upload-endpoint).

- [Validate Dataset Upload](https://docs.fireworks.ai/api-reference/validate-dataset-upload.md)
- [Validate Evaluator Upload](https://docs.fireworks.ai/api-reference/validate-evaluator-upload.md): Triggers server-side validation of the uploaded source code (**step 5** in
the [Create Evaluator](/api-reference/create-evaluator) workflow). The server
extracts and processes the archive, then builds the evaluator environment.
Poll [Get Evaluator](/api-reference/get-evaluator) to monitor progress.
- [Validate Model Upload](https://docs.fireworks.ai/api-reference/validate-model-upload.md)
- [Autoscaling](https://docs.fireworks.ai/deployments/autoscaling.md): Configure how your deployment scales based on traffic
- [Performance benchmarking](https://docs.fireworks.ai/deployments/benchmarking.md): Measure and optimize your deployment's performance with load testing
- [Client-side performance optimization](https://docs.fireworks.ai/deployments/client-side-performance-optimization.md): Optimize your client code for maximum performance with dedicated deployments
- [Direct routing](https://docs.fireworks.ai/deployments/direct-routing.md): Direct routing enables enterprise users reduce latency to their deployments.
- [Exporting Metrics](https://docs.fireworks.ai/deployments/exporting-metrics.md): Export metrics from your dedicated deployments to your observability stack
- [Regions](https://docs.fireworks.ai/deployments/regions.md): Fireworks runs a global fleet of hardware on which you can deploy your models.
- [Reserved capacity](https://docs.fireworks.ai/deployments/reservations.md)
- [Speculative Decoding](https://docs.fireworks.ai/deployments/speculative-decoding.md): Speed up generation with draft models and n-gram speculation
- [Cloud Integrations](https://docs.fireworks.ai/ecosystem/integrations.md): Cloud Integrations
- [Agent Frameworks](https://docs.fireworks.ai/ecosystem/integrations/agent-frameworks.md): Build production-ready AI agents with Fireworks and leading open-source frameworks
- [MLOps & Observability](https://docs.fireworks.ai/ecosystem/integrations/mlops-observability.md): Track and monitor your Fireworks AI deployments with leading MLOps and observability platforms
- [Cookbooks](https://docs.fireworks.ai/examples/cookbooks.md): Interactive Jupyter notebooks demonstrating advanced use cases and best practices with Fireworks AI
- [Courses](https://docs.fireworks.ai/examples/introduction.md): Standalone end-to-end examples showing how to use Fireworks to solve real-world use cases
- [How do I close my Fireworks.ai account?](https://docs.fireworks.ai/faq-new/account-access/how-do-i-close-my-fireworksai-account.md)
- [I have multiple Fireworks accounts. When I try to login with Google on Fireworks' web UI, I'm getting signed into the wrong account. How do I fix this?](https://docs.fireworks.ai/faq-new/account-access/i-have-multiple-fireworks-accounts-when-i-try-to-login-with-google-on-fireworks.md)
- [What email does GitHub authentication use?](https://docs.fireworks.ai/faq-new/account-access/what-email-does-github-authentication-use.md)
- [What email does LinkedIn authentication use?](https://docs.fireworks.ai/faq-new/account-access/what-email-does-linkedin-authentication-use.md)
- [What should I do if I can't access my company account after being invited when I already have a personal account?](https://docs.fireworks.ai/faq-new/account-access/what-should-i-do-if-i-cant-access-my-company-account-after-being-invited-when-i.md)
- [Are there discounts for bulk usage?](https://docs.fireworks.ai/faq-new/billing-pricing/are-there-discounts-for-bulk-usage.md)
- [Are there extra fees for serving fine-tuned models?](https://docs.fireworks.ai/faq-new/billing-pricing/are-there-extra-fees-for-serving-fine-tuned-models.md)
- [How does billing and credit usage work?](https://docs.fireworks.ai/faq-new/billing-pricing/how-does-billing-and-credit-usage-work.md)
- [How many tokens per image?](https://docs.fireworks.ai/faq-new/billing-pricing/how-many-tokens-per-image.md): Learn how to calculate token usage for images in vision models and understand pricing implications
- [How much does Fireworks cost?](https://docs.fireworks.ai/faq-new/billing-pricing/how-much-does-fireworks-cost.md)
- [Is prompt caching billed differently for serverless models?](https://docs.fireworks.ai/faq-new/billing-pricing/is-prompt-caching-billed-differently.md)
- [How do credits work?](https://docs.fireworks.ai/faq-new/billing-pricing/what-happens-when-i-finish-my-1-dollar-credit.md)
- [Why might my account be suspended even with remaining credits?](https://docs.fireworks.ai/faq-new/billing-pricing/why-might-my-account-be-suspended-even-with-remaining-credits.md)
- [Are there any quotas for serverless?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/are-there-any-quotas-for-serverless.md)
- [Do you provide notice before removing model availability?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/do-you-provide-notice-before-removing-model-availability.md)
- [Do you support Auto Scaling?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/do-you-support-auto-scaling.md)
- [How does autoscaling affect my costs?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/how-does-autoscaling-affect-my-costs.md)
- [How does billing and scaling work for on-demand GPU deployments?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/how-does-billing-and-scaling-work-for-on-demand-gpu-deployments.md)
- [How does billing work for on-demand deployments?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/how-does-billing-work-for-on-demand-deployments.md)
- [How does the system scale?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/how-does-the-system-scale.md)
- [Are there SLAs for serverless?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/is-latency-guaranteed-for-serverless-models.md)
- [What are the rate limits for on-demand deployments?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/what-are-the-rate-limits-for-on-demand-deployments.md)
- [What factors affect the number of simultaneous requests that can be handled?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/what-factors-affect-the-number-of-simultaneous-requests-that-can-be-handled.md)
- [What’s the supported throughput?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/whats-the-supported-throughput.md)
- [Why am I experiencing request timeout errors and slow response times with serverless LLM models?](https://docs.fireworks.ai/faq-new/deployment-infrastructure/why-am-i-experiencing-request-timeout-errors-and-slow-response-times-with-server.md)
- [Does Fireworks support custom base models?](https://docs.fireworks.ai/faq-new/models-inference/does-fireworks-support-custom-base-models.md)
- [Does the API support batching and load balancing?](https://docs.fireworks.ai/faq-new/models-inference/does-the-api-support-batching-and-load-balancing.md)
- [FLUX image generation](https://docs.fireworks.ai/faq-new/models-inference/flux-image-generation.md)
- [How do I control output image sizes when using SDXL ControlNet?](https://docs.fireworks.ai/faq-new/models-inference/how-do-i-control-output-image-sizes-when-using-sdxl-controlnet.md)
- [How to check if a model is available on serverless?](https://docs.fireworks.ai/faq-new/models-inference/how-to-check-if-a-model-is-available-on-serverless.md)
- [There’s a model I would like to use that isn’t available on Fireworks. Can I request it?](https://docs.fireworks.ai/faq-new/models-inference/theres-a-model-i-would-like-to-use-that-isnt-available-on-fireworks-can-i-reques.md)
- [What factors affect the number of simultaneous requests that can be handled?](https://docs.fireworks.ai/faq-new/models-inference/what-factors-affect-the-number-of-simultaneous-requests-that-can-be-handled.md)
- [Training Overview](https://docs.fireworks.ai/fine-tuning/cli-reference.md): Launch RFT jobs using the eval-protocol CLI
- [Remote Environment Setup](https://docs.fireworks.ai/fine-tuning/connect-environments.md): Implement the /init endpoint to run evaluations in your infrastructure
- [Deploying Fine Tuned Models](https://docs.fireworks.ai/fine-tuning/deploying-loras.md): Deploy one or multiple LoRA models fine tuned on Fireworks
- [Direct Preference Optimization](https://docs.fireworks.ai/fine-tuning/dpo-fine-tuning.md)
- [Agent Tracing](https://docs.fireworks.ai/fine-tuning/environments.md): Understand where your agent runs and how tracing enables reinforcement fine-tuning
- [Evaluators](https://docs.fireworks.ai/fine-tuning/evaluators.md): Understand the fundamentals of evaluators and reward functions in reinforcement fine-tuning
- [Supervised Fine Tuning - Text](https://docs.fireworks.ai/fine-tuning/fine-tuning-models.md)
- [Supervised Fine Tuning - Vision](https://docs.fireworks.ai/fine-tuning/fine-tuning-vlm.md): Learn how to fine-tune vision-language models on Fireworks AI with image and text datasets
- [Fine Tuning Overview](https://docs.fireworks.ai/fine-tuning/finetuning-intro.md)
- [Basics](https://docs.fireworks.ai/fine-tuning/how-rft-works.md): Understand the reinforcement learning fundamentals behind RFT
- [Monitor Training](https://docs.fireworks.ai/fine-tuning/monitor-training.md): Track RFT job progress and diagnose issues in real-time
- [Parameter Tuning](https://docs.fireworks.ai/fine-tuning/parameter-tuning.md): Learn how training parameters affect model behavior and outcomes
- [Single-Turn Training Quickstart](https://docs.fireworks.ai/fine-tuning/quickstart-math.md): Train a model to be an expert at answering GSM8K math questions
- [Remote Agent Quickstart](https://docs.fireworks.ai/fine-tuning/quickstart-svg-agent.md): Train an SVG drawing agent running in a remote environment
- [Overview](https://docs.fireworks.ai/fine-tuning/reinforcement-fine-tuning-models.md): Train models using reinforcement learning in minutes
- [Secure Training (BYOB)](https://docs.fireworks.ai/fine-tuning/secure-fine-tuning.md): Fine-tune models while keeping sensitive data and components under your control
- [Training Prerequisites & Validation](https://docs.fireworks.ai/fine-tuning/training-prerequisites.md): Requirements, validation checks, and common issues when launching RFT jobs
- [Using Secrets](https://docs.fireworks.ai/fine-tuning/using-secret-in-evaluator.md): Learn how to create secrets that can be utilized within your reward function.
- [Warm Start from Fine-Tuned Models](https://docs.fireworks.ai/fine-tuning/warm-start.md): Continue training from a previously fine-tuned model with RFT
- [Training Guide: UI](https://docs.fireworks.ai/fine-tuning/web-ui-guide.md): Launch RFT jobs using the Fireworks dashboard
- [Weighted Training](https://docs.fireworks.ai/fine-tuning/weighted-training.md): Control which samples have greater influence during RFT training
- [Concepts](https://docs.fireworks.ai/getting-started/concepts.md): This document outlines basic Fireworks AI concepts.
- [Build with Fireworks AI](https://docs.fireworks.ai/getting-started/introduction.md): Fast inference and fine-tuning for open source models
- [Deployments Quickstart](https://docs.fireworks.ai/getting-started/ondemand-quickstart.md): Deploy models on dedicated GPUs in minutes
- [Serverless Quickstart](https://docs.fireworks.ai/getting-started/quickstart.md): Make your first Serverless API call in minutes
- [Batch API](https://docs.fireworks.ai/guides/batch-inference.md): Process large-scale async workloads
- [Completions API](https://docs.fireworks.ai/guides/completions-api.md): Use the completions API for raw text generation with custom prompt templates
- [Tool Calling](https://docs.fireworks.ai/guides/function-calling.md): Connect models to external tools and APIs
- [Inference Error Codes](https://docs.fireworks.ai/guides/inference-error-codes.md): Common error codes, their meanings, and resolutions for inference requests
- [Deployments](https://docs.fireworks.ai/guides/ondemand-deployments.md): Configure and manage on-demand deployments on dedicated GPUs
- [Using predicted outputs](https://docs.fireworks.ai/guides/predicted-outputs.md): Use Predicted Outputs to boost output generation speeds for editing / rewriting use cases
- [Prompt caching](https://docs.fireworks.ai/guides/prompt-caching.md)
- [Speech to Text](https://docs.fireworks.ai/guides/querying-asr-models.md): Convert audio to text with streaming and pre-recorded transcription
- [Embeddings & Reranking](https://docs.fireworks.ai/guides/querying-embeddings-models.md): Generate embeddings and rerank results for semantic search
- [Text Models](https://docs.fireworks.ai/guides/querying-text-models.md): Query, track and manage inference for text models
- [Vision Models](https://docs.fireworks.ai/guides/querying-vision-language-models.md): Query vision-language models to analyze images and visual content
- [Rate Limits & Quotas](https://docs.fireworks.ai/guides/quotas_usage/rate-limits.md): Understand and manage your rate limits, spend limits and quotas
- [Reasoning](https://docs.fireworks.ai/guides/reasoning.md): How to use reasoning with Fireworks models
- [Which model should I use?](https://docs.fireworks.ai/guides/recommended-models.md): Find the best open models for your use case or migrate from closed source models like Claude, GPT, and Gemini
- [Responses API](https://docs.fireworks.ai/guides/response-api.md)
- [Audit & Access Logs](https://docs.fireworks.ai/guides/security_compliance/audit_logs.md): Monitor and track account activities with audit logging for Enterprise accounts
- [Zero Data Retention](https://docs.fireworks.ai/guides/security_compliance/data_handling.md): Data retention policies at Fireworks
- [Data Security](https://docs.fireworks.ai/guides/security_compliance/data_security.md): How we secure and handle your data for inference and training
- [Video & Audio Inputs](https://docs.fireworks.ai/guides/video-audio-inputs.md): Query multimodal models to process video and audio content directly
- [Quantization](https://docs.fireworks.ai/models/quantization.md): Reduce model precision to improve performance and lower costs
- [Custom Models](https://docs.fireworks.ai/models/uploading-custom-models.md): Upload, verify, and deploy your own models from Hugging Face or elsewhere
- [Structured Outputs](https://docs.fireworks.ai/structured-responses/structured-response-formatting.md): Enforce output formats using JSON schemas or custom grammars
- [firectl account get](https://docs.fireworks.ai/tools-sdks/firectl/commands/account-get.md): Prints information about an account.
- [firectl account list](https://docs.fireworks.ai/tools-sdks/firectl/commands/account-list.md): Prints all accounts the current signed-in user has access to.
- [firectl api-key create](https://docs.fireworks.ai/tools-sdks/firectl/commands/api-key-create.md): Creates an API key for the signed in user or a specified service account user.
- [firectl api-key delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/api-key-delete.md): Deletes an API key.
- [firectl api-key list](https://docs.fireworks.ai/tools-sdks/firectl/commands/api-key-list.md): Prints all API keys for the signed in user.
- [Authentication](https://docs.fireworks.ai/tools-sdks/firectl/commands/authentication.md): Authentication for access to your account
- [firectl batch-inference-job create](https://docs.fireworks.ai/tools-sdks/firectl/commands/batch-inference-job-create.md): Creates a batch inference job.
- [firectl batch-inference-job delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/batch-inference-job-delete.md): Deletes a batch inference job.
- [firectl batch-inference-job get](https://docs.fireworks.ai/tools-sdks/firectl/commands/batch-inference-job-get.md): Retrieves information about a batch inference job.
- [firectl batch-inference-job list](https://docs.fireworks.ai/tools-sdks/firectl/commands/batch-inference-job-list.md): Lists all batch inference jobs in an account.
- [firectl billing export-metrics](https://docs.fireworks.ai/tools-sdks/firectl/commands/billing-export-metrics.md): Exports billing metrics
- [firectl billing list-invoices](https://docs.fireworks.ai/tools-sdks/firectl/commands/billing-list-invoices.md): Prints information about invoices.
- [firectl credit-redemption list](https://docs.fireworks.ai/tools-sdks/firectl/commands/credit-redemption-list.md): Lists credit code redemptions for the current account.
- [firectl credit-redemption redeem](https://docs.fireworks.ai/tools-sdks/firectl/commands/credit-redemption-redeem.md): Redeems a credit code.
- [firectl dataset create](https://docs.fireworks.ai/tools-sdks/firectl/commands/dataset-create.md): Creates and uploads a dataset.
- [firectl dataset delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/dataset-delete.md): Deletes a dataset.
- [firectl dataset download](https://docs.fireworks.ai/tools-sdks/firectl/commands/dataset-download.md): Downloads a dataset to a local directory.
- [firectl dataset get](https://docs.fireworks.ai/tools-sdks/firectl/commands/dataset-get.md): Prints information about a dataset.
- [firectl dataset list](https://docs.fireworks.ai/tools-sdks/firectl/commands/dataset-list.md): Prints all datasets in an account.
- [firectl dataset update](https://docs.fireworks.ai/tools-sdks/firectl/commands/dataset-update.md): Updates a dataset.
- [firectl deployed-model get](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployed-model-get.md): Prints information about a deployed model.
- [firectl deployed-model list](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployed-model-list.md): Prints all deployed models in the account.
- [firectl deployed-model update](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployed-model-update.md): Update a deployed model.
- [firectl deployment create](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-create.md): Creates a new deployment.
- [firectl deployment delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-delete.md): Deletes a deployment.
- [firectl deployment get](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-get.md): Prints information about a deployment.
- [firectl deployment list](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-list.md): Prints all deployments in the account.
- [firectl deployment scale](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-scale.md): Scales a deployment to a specified number of replicas.
- [firectl deployment-shape-version get](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-shape-version-get.md): Prints information about a deployment shape version.
- [firectl deployment-shape-version list](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-shape-version-list.md): Prints all deployment shape versions of this deployment shape.
- [firectl deployment undelete](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-undelete.md): Undeletes a deployment.
- [firectl deployment update](https://docs.fireworks.ai/tools-sdks/firectl/commands/deployment-update.md): Update a deployment.
- [firectl dpo-job cancel](https://docs.fireworks.ai/tools-sdks/firectl/commands/dpo-job-cancel.md): Cancels a running dpo job.
- [firectl dpo-job create](https://docs.fireworks.ai/tools-sdks/firectl/commands/dpo-job-create.md): Creates a dpo job.
- [firectl dpo-job delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/dpo-job-delete.md): Deletes a dpo job.
- [firectl dpo-job export-metrics](https://docs.fireworks.ai/tools-sdks/firectl/commands/dpo-job-export-metrics.md): Exports metrics for a dpo job.
- [firectl dpo-job get](https://docs.fireworks.ai/tools-sdks/firectl/commands/dpo-job-get.md): Retrieves information about a dpo job.
- [firectl dpo-job list](https://docs.fireworks.ai/tools-sdks/firectl/commands/dpo-job-list.md): Lists all dpo jobs in an account.
- [firectl dpo-job resume](https://docs.fireworks.ai/tools-sdks/firectl/commands/dpo-job-resume.md): Resumes a dpo job.
- [firectl evaluator-revision alias](https://docs.fireworks.ai/tools-sdks/firectl/commands/evaluator-revision-alias.md): Alias an evaluator revision
- [firectl evaluator-revision delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/evaluator-revision-delete.md): Delete an evaluator revision
- [firectl evaluator-revision get](https://docs.fireworks.ai/tools-sdks/firectl/commands/evaluator-revision-get.md): Get an evaluator revision
- [firectl evaluator-revision list](https://docs.fireworks.ai/tools-sdks/firectl/commands/evaluator-revision-list.md): List evaluator revisions
- [firectl identity-provider create](https://docs.fireworks.ai/tools-sdks/firectl/commands/identity-provider-create.md): Creates a new identity provider.
- [firectl identity-provider get](https://docs.fireworks.ai/tools-sdks/firectl/commands/identity-provider-get.md): Prints information about an identity provider.
- [firectl identity-provider list](https://docs.fireworks.ai/tools-sdks/firectl/commands/identity-provider-list.md): List identity providers for an account
- [firectl model create](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-create.md): Creates and uploads a model.
- [firectl model delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-delete.md): Deletes a model.
- [firectl model download](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-download.md): Download a model.
- [firectl model get](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-get.md): Prints information about a model.
- [firectl model list](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-list.md): Prints all models in an account.
- [firectl model load-lora](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-load-lora.md): Loads a LoRA model.
- [firectl model prepare](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-prepare.md): Prepare models for different precisions
- [firectl model unload-lora](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-unload-lora.md): Unloads a LoRA model.
- [firectl model update](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-update.md): Updates a model.
- [firectl model upload](https://docs.fireworks.ai/tools-sdks/firectl/commands/model-upload.md): Resumes or completes a model upload.
- [firectl quota get](https://docs.fireworks.ai/tools-sdks/firectl/commands/quota-get.md): Prints information about a quota.
- [firectl quota list](https://docs.fireworks.ai/tools-sdks/firectl/commands/quota-list.md): Prints all quotas.
- [firectl quota update](https://docs.fireworks.ai/tools-sdks/firectl/commands/quota-update.md): Updates a quota.
- [firectl reinforcement-fine-tuning-job cancel](https://docs.fireworks.ai/tools-sdks/firectl/commands/reinforcement-fine-tuning-job-cancel.md): Cancels a running reinforcement fine-tuning job.
- [firectl reinforcement-fine-tuning-job create](https://docs.fireworks.ai/tools-sdks/firectl/commands/reinforcement-fine-tuning-job-create.md): Creates a reinforcement fine-tuning job.
- [firectl reinforcement-fine-tuning-job delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/reinforcement-fine-tuning-job-delete.md): Deletes a reinforcement fine-tuning job.
- [firectl reinforcement-fine-tuning-job get](https://docs.fireworks.ai/tools-sdks/firectl/commands/reinforcement-fine-tuning-job-get.md): Retrieves information about a reinforcement fine-tuning job.
- [firectl reinforcement-fine-tuning-job list](https://docs.fireworks.ai/tools-sdks/firectl/commands/reinforcement-fine-tuning-job-list.md): Lists all reinforcement fine-tuning jobs in an account.
- [firectl reinforcement-fine-tuning-job resume](https://docs.fireworks.ai/tools-sdks/firectl/commands/reinforcement-fine-tuning-job-resume.md): Resumes a failed reinforcement fine-tuning job.
- [firectl reservation get](https://docs.fireworks.ai/tools-sdks/firectl/commands/reservation-get.md): Prints information about a reservation.
- [firectl reservation list](https://docs.fireworks.ai/tools-sdks/firectl/commands/reservation-list.md): Prints active reservations.
- [firectl secret create](https://docs.fireworks.ai/tools-sdks/firectl/commands/secret-create.md): Creates a secret for the signed in user.
- [firectl secret delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/secret-delete.md): Deletes a secret.
- [firectl secret get](https://docs.fireworks.ai/tools-sdks/firectl/commands/secret-get.md): Retrieves a secret by name.
- [firectl secret list](https://docs.fireworks.ai/tools-sdks/firectl/commands/secret-list.md): Lists all secrets for the signed in user.
- [firectl secret update](https://docs.fireworks.ai/tools-sdks/firectl/commands/secret-update.md): Updates an existing secret.
- [firectl set-api-key](https://docs.fireworks.ai/tools-sdks/firectl/commands/set-api-key.md): Sets the default API key in ~/.fireworks/auth.ini.
- [firectl supervised-fine-tuning-job cancel](https://docs.fireworks.ai/tools-sdks/firectl/commands/supervised-fine-tuning-job-cancel.md): Cancels a running supervised fine-tuning job.
- [firectl supervised-fine-tuning-job create](https://docs.fireworks.ai/tools-sdks/firectl/commands/supervised-fine-tuning-job-create.md): Creates a supervised fine-tuning job.
- [firectl supervised-fine-tuning-job delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/supervised-fine-tuning-job-delete.md): Deletes a supervised fine-tuning job.
- [firectl supervised-fine-tuning-job get](https://docs.fireworks.ai/tools-sdks/firectl/commands/supervised-fine-tuning-job-get.md): Retrieves information about a supervised fine-tuning job.
- [firectl supervised-fine-tuning-job list](https://docs.fireworks.ai/tools-sdks/firectl/commands/supervised-fine-tuning-job-list.md): Lists all supervised fine-tuning jobs in an account.
- [firectl upgrade](https://docs.fireworks.ai/tools-sdks/firectl/commands/upgrade.md): Upgrades the firectl binary to the latest version.
- [firectl user create](https://docs.fireworks.ai/tools-sdks/firectl/commands/user-create.md): Creates a new user.
- [firectl user delete](https://docs.fireworks.ai/tools-sdks/firectl/commands/user-delete.md): Deletes a user.
- [firectl user get](https://docs.fireworks.ai/tools-sdks/firectl/commands/user-get.md): Prints information about a user.
- [firectl user list](https://docs.fireworks.ai/tools-sdks/firectl/commands/user-list.md): Prints all users in the account.
- [firectl user update](https://docs.fireworks.ai/tools-sdks/firectl/commands/user-update.md): Updates a user.
- [firectl version](https://docs.fireworks.ai/tools-sdks/firectl/commands/version.md): Prints the version of firectl
- [firectl whoami](https://docs.fireworks.ai/tools-sdks/firectl/commands/whoami.md): Shows the currently authenticated user
- [Getting started](https://docs.fireworks.ai/tools-sdks/firectl/firectl.md): Learn to create, deploy, and manage resources using Firectl
- [OpenAI compatibility](https://docs.fireworks.ai/tools-sdks/openai-compatibility.md)
- [Querying Dedicated Deployments](https://docs.fireworks.ai/tools-sdks/python-client/querying-dedicated-deployments.md): Learn how to connect to and query dedicated deployments that were created outside the SDK
- [Build SDK Basics](https://docs.fireworks.ai/tools-sdks/python-client/sdk-basics.md)
- [Build SDK Introduction](https://docs.fireworks.ai/tools-sdks/python-client/sdk-introduction.md)
- [Reference](https://docs.fireworks.ai/tools-sdks/python-client/sdk-reference.md)
- [Tutorial](https://docs.fireworks.ai/tools-sdks/python-client/the-tutorial.md)
- [Python SDK](https://docs.fireworks.ai/tools-sdks/python-sdk.md)
- [Changelog](https://docs.fireworks.ai/updates/changelog.md)


## Optional

- [Demos](https://demos.fireworks.ai)
