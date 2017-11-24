author1 = {'firstname': 'Ronald', 'lastname': 'Cramer'}
author2 = {'firstname': 'Victor', 'lastname': 'Shoup'}

author1_str = f'{author1["firstname"]} {author1["lastname"]}'
author2_str = f'{author2["firstname"]} {author2["lastname"]}'

paper1 = {
    'title': 'Universal Hash Proofs and a Paradigm for Adaptive Chosen Ciphertext Secure Public-Key Encryption',
    'year': 2001,
    'pages': 40,
    'authors': [author1, author2],
    'hash': '94ac2fc3d6f7ade3419b2fb1d950b3840542717031c5e7e32491c30b5eb2356c'
}

paper2 = {
    'title': 'Sequences of Games: A Tool for Taming Complexity in Security Proofs',
    'year': 2006,
    'pages': 33,
    'authors': [author2],
    'hash': 'fde1f65e83ec85297f58840bf87de15fb68e91ada8aefaf77db3b153cf826820'
}
