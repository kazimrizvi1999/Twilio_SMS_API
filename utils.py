import json

def split_numbers(arr, num_threads = 5):
    chunk_size = len(arr)//num_threads
    split_numbers = []

    for idx in range(0, len(arr), chunk_size):
        split = arr[idx : idx+chunk_size]
        split_numbers.append(split)
    
    if len(split_numbers) > num_threads:
        split_numbers[-2].extend(split_numbers.pop(-1))

    return split_numbers

def preprocess_data(byte_data):
    data = byte_data.decode('utf-8').replace("'", '"')
    json_data = json.loads(data)
    return json_data

def launch_sms(client, numbers, message_body, sender, process_id):
    for number in numbers:
        message = client.messages \
        .create(
            body=message_body,
            from_=sender,
            to=number
        )
        print(f"\nProcess#{process_id}\tNumber:{number}\tMessageSID:{message.sid}\t")
    print(f"\nProcess# {process_id} COMPLETED!")