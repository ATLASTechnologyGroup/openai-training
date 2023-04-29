# OpenAI Fine-Tuning

This project is a Python script that uses the OpenAI API to fine-tune a model on a given training data file.

## Requirements

- An OpenAI API key: https://beta.openai.com/docs/api-reference/authentication

## Usage

There are two ways to run this project: using Docker or using Python.

### Using Docker

Docker is a tool that allows you to run applications in isolated and portable environments. You can use Docker to run this project without worrying about dependencies or compatibility issues.

To run the project using Docker, use the following steps:

1. Install Docker on your machine: https://docs.docker.com/get-docker/
2. Load the Docker image from the tar file using this command:

`docker load < openai-training-image.tar`

This will create an image called `openai_training_image` on your machine.
3. Either:
- Create a file called `openai_api_key.txt` in any directory of your choice, and paste your OpenAI API key in it
- Create a Docker secret called `openai_api_key` that contains your OpenAI API key using this command:
`echo "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" | docker secret create openai_api_key -`
where `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` is your OpenAI API key.
4. Run the Docker container using the first command if you made a file, or the second command if you made a secret:

- `docker run -it -v /path/to/openai_api_key.txt:/run/secrets/openai_api_key your_username/openai-fine-tuning model_id training_data_path n_epochs [timeout]`
- `docker run -it --secret openai_api_key your_username/openai-fine-tuning model_id training_data_path n_epochs [timeout]`

Where:

- `/path/to/openai_api_key.txt` is the absolute path to the file that contains your OpenAI API key.
- `model_id` is the ID of the model to fine-tune, or `None` to use the default `davinci` model.
- `training_data_path` is the path to the training data file in JSONL format.
- `n_epochs` is the number of epochs to train the model for.
- `timeout` is an optional argument that specifies the maximum time (in seconds) to wait for the fine-tuning to complete. The default value is 300 seconds.

The script will upload the training data file to OpenAI's servers, fine-tune the model, and print the ID of the fine-tuned model.

### Using Python

Python is a popular programming language that you can use to run this project directly on your machine. You need to install Python and some libraries before running the script.

To run the project using Python, use the following steps:

1. Install Python 3.11 on your machine: https://www.python.org/downloads/
2. Install OpenAI Python library using this command:

`pip install openai`

3. Set your OpenAI API key as an environment variable or create a file that contains it:

- To set it as an environment variable, use this command:

`export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

where `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` is your OpenAI API key.

- To create a file that contains it, create a file called `openai_api_key.txt` in the same directory as your script, and paste your OpenAI API key in it.

4. Clone or download this repository to your local machine.
5. Run the script using this command:

`python train_model.py model_id training_data_path n_epochs [timeout]`

where:

- `model_id` is the ID of the model to fine-tune, or `None` to use the default `davinci` model.
- `training_data_path` is the path to the training data file in JSONL format.
- `n_epochs` is the number of epochs to train the model for.
- `timeout` is an optional argument that specifies the maximum time (in seconds) to wait for the fine-tuning to complete. The default value is 300 seconds.

The script will upload the training data file to OpenAI's servers, fine-tune the model, and print the ID of the fine-tuned model.

## Example

To fine-tune the `curie` model on a file called `data.jsonl` for 10 epochs, with a timeout of 600 seconds, use this command:

Using Docker:

`docker run -it -v /path/to/openai_api_key.txt:/run/secrets/openai_api_key your_username/openai-fine-tuning curie data.jsonl 10 600`

`docker run -it --secret openai_api_key your_username/openai-fine-tuning curie data.jsonl 10 600`

Using Python:

`python train_model.py curie data.jsonl 10 600`