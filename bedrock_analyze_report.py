# Use the Converse API to send a text message to Claude 3 Opus.

import boto3
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Titan Text Premier.
model_id = "anthropic.claude-3-opus-20240229-v1:0"

# Start a conversation with the user message.
user_message = """Your task is to analyze the following report:
<report>
{{FULL REPORT TEXT FROM https://investors.matterport.com/node/9501/html}}
</report>

Summarize this annual report in a concise and clear manner, and identify key market trends and takeaways. Output your findings as a short memo I can send to my team. The goal of the memo is to ensure my team stays up to date on how financial institutions are faring and qualitatively forecast and identify whether there are any operating and revenue risks to be expected in the coming quarter. Make sure to include all relevant details in your summary and analysis."""
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId="anthropic.claude-3-opus-20240229-v1:0",
        messages=conversation,
        inferenceConfig={"maxTokens":4096,"temperature":0},
        additionalModelRequestFields={"top_k":250}
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
