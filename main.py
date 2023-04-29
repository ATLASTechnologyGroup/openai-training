import os
import sys
import time
import openai


def print_usage():
    print('Usage: python main.py <model_id> <file_path> <n_epochs> [timeout]')
    print()
    print('Arguments:')
    print('  model_id: ID of the model to fine-tune (use "None" to create a new model)')
    print('  file_path: Path to the training data file (must be in JSONL format)')
    print('  n_epochs: Number of epochs to fine-tune the model for')
    print('  timeout: (optional) Maximum time to wait for fine-tuning to complete (in seconds)')
    print()
    print('Example:')
    print('  python main.py model-123 /path/to/training_data.jsonl 1 300')
    print()
    print('If on Windows, you need to provide the file key as a mounted file at /app/openai_api_key.txt, otherwise, use Docker secrets')
    print()
    print('Example on Windows:')
    print(r'  -v C:\Users\windows.user\Documents\openai_api_key.txt:/app/openai_api_key.txt')


def train_model(model_id, training_data_path, n_epochs, timeout):
    # Upload the file to OpenAI's servers
    with open(training_data_path) as training_data:
        file = openai.File.create(file=training_data, purpose='fine-tune')

    # Fine-tune a model using the uploaded file
    if model_id is None:
        model = openai.FineTune.create(
            training_file=file['id'],
            model='davinci',
            n_epochs=n_epochs
        )
    else:
        model = openai.FineTune.create(
            training_file=file['id'],
            model=model_id,
            n_epochs=n_epochs
        )

    # Wait for the fine-tuning to complete
    start_time = time.time()
    while model['status'] != 'succeeded':
        if time.time() - start_time > timeout:
            raise Exception('Fine-tuning timed out')

        time.sleep(5)
        model = openai.FineTune.retrieve(model['id'])

    print(model['fine_tuned_model'])


if __name__ == '__main__':
    if len(sys.argv) < 4\
            or len(sys.argv) > 5\
            or '--help' in sys.argv:
        print_usage()
        sys.exit(1)

    try:
        model_id_arg = sys.argv[1]
        if model_id_arg.lower() == 'none':
            model_id_arg = None

        file_path_arg = sys.argv[2]
        n_epochs_arg = int(sys.argv[3])
        timeout_arg = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    except ValueError as e:
        print(f'Invalid argument provided: {e}')
        print()
        print_usage()
        sys.exit(1)

    env_api_key = os.getenv("OPENAI_API_KEY")
    if env_api_key:
        openai.api_key = env_api_key
    else:
        with open('/app/openai_api_key.txt', 'r') as api_key:
            openai.api_key = api_key.read().strip()

    train_model(model_id_arg, file_path_arg, n_epochs_arg, timeout_arg)
