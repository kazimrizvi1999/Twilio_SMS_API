import json

def validate(numbers):
    verified_nums=[]
    for i in numbers:
        if len(i)==12 and i.startswith('+'):
            verified_nums.append(i)
    return verified_nums

# dummy_nums=['+143626366223','+1264728487363764376476','+12345678901','+098276453215','123457132341']
# a=validate(dummy_nums)
# print(a)



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