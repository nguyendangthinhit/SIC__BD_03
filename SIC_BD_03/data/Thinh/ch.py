def fb_base58_decode(s):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    base_count = len(alphabet)
    decoded = 0
    multi = 1
    for char in s[::-1]:
        if char not in alphabet:
            continue  # bỏ qua ký tự không hợp lệ
        index = alphabet.find(char)
        decoded += multi * index
        multi *= base_count
    return decoded

def decode_pfbid(pfbid):
    if not pfbid.startswith('pfbid'):
        raise ValueError("Not a valid pfbid")
    pfbid_base58 = pfbid[5:]
    num = fb_base58_decode(pfbid_base58)
    return str(num)[-16:]

# Test
pfbid1 = "pfbid02G1fszqS6RM6peF1QWZEt3eytima1cn3LpiLoTpjudJUPkhsW4of4vepdj642WFSMl"
pfbid2 = "pfbid02GBptHyhqF4jhftc4QD8VnVyriD33tUD8wc2QpaxrdpLzGxEYDXCJLDYsB9Vrv6jbl"

print("Post ID 1:", decode_pfbid(pfbid1))
print("Post ID 2:", decode_pfbid(pfbid2))
