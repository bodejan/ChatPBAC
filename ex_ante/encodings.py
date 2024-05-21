# Define the purposes
purposes = [
    {
        'name': 'General-Purpose',
        'id': 1,
        'parent_id': None,
        'code': 1,
        'aip_code': 8191,
        'pip_code': 8191
    },
    {
        'name': 'Clinical-Care',
        'id': 2,
        'parent_id': 1,
        'code': 2,
        'aip_code': 2,
        'pip_code': 3
    },
    {
        'name': 'Research',
        'id': 3,
        'parent_id': 1,
        'code': 4,
        'aip_code': 124,
        'pip_code': 125
    },
    {
        'name': 'Public-Research',
        'id': 4,
        'parent_id': 3,
        'code': 8,
        'aip_code': 56,
        'pip_code': 61
    },
    {
        'name': 'Military-Research',
        'id': 5,
        'parent_id': 4,
        'code': 16,
        'aip_code': 16,
        'pip_code': 29
    },
    {
        'name': 'Non-Military-Research',
        'id': 6,
        'parent_id': 4,
        'code': 32,
        'aip_code': 32,
        'pip_code': 45
    },
    {
        'name': 'Private-Research',
        'id': 7,
        'parent_id': 3,
        'code': 64,
        'aip_code': 64,
        'pip_code': 69
    },
    {
        'name': 'Patient-Support-Service',
        'id': 8,
        'parent_id': 1,
        'code': 128,
        'aip_code': 896,
        'pip_code': 897
    },
    {
        'name': 'Billing',
        'id': 9,
        'parent_id': 8,
        'code': 256,
        'aip_code': 256,
        'pip_code': 385
    },
    {
        'name': 'Communication',
        'id': 10,
        'parent_id': 8,
        'code': 512,
        'aip_code': 512,
        'pip_code': 641
    },
    {
        'name': 'Third-Party',
        'id': 11,
        'parent_id': 1,
        'code': 1024,
        'aip_code': 7168,
        'pip_code': 7169
    },
    {
        'name': 'Marketing',
        'id': 12,
        'parent_id': 11,
        'code': 2048,
        'aip_code': 2048,
        'pip_code': 3073
    },
    {
        'name': 'Product-Development',
        'id': 13,
        'parent_id': 11,
        'code': 4096,
        'aip_code': 4096,
        'pip_code': 5121
    },
]


def encode_purposes(purpose_codes: list[int]):
    """Encode a list of purpose codes into a single integer.
    For allowed intended purposes, provide the node itself and all its children. 
    For prohibited intended purposes, provide the node itself, all ancestors, and children.
    """
    encoded_int = 0
    for purpose in purposes:
        if purpose['code'] in purpose_codes:
            encoded_int |= purpose['code']
    return encoded_int


def decode_purposes(encoded_int: int, purposes: list[dict]):
    """Decode an integer into a list of purpose names."""
    decoded_purposes = []
    for purpose in purposes:
        if encoded_int & purpose['code']:
            decoded_purposes.append(purpose['name'])
    return decoded_purposes


def create_purpose_codes(number_of_purposes: int):
    """Create a list of purpose codes from the given number of purposes."""
    purpose_codes = []
    for i in range(number_of_purposes):
        purpose_codes.append(2 ** i)
    return purpose_codes


def check_compliance(access_code, aip, pip):
    return (access_code & pip == 0) and (access_code & aip != 0)


print(check_compliance(4, 8191, 0))  # True
