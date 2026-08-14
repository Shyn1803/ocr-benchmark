![](<05d9fd5d99ac557f1dfa74c097f7c1cbc9b34be0_page_6_images/imageFile1.png>)

# Cont… (distributiontime)

## In P2P architecture:

• In P2P, when a peer receives some file data, it can use its own upload capacity to redistribute the data to other peers.

Calculating the distribution time for the P2P architecture is somewhat more complicated. A simple expression for the minimal distribution time:

- • Step1: At the beginning, only the server has the file.
- • To get this file into the community of peers, minimum distribution time is at least F/us.
- • Step2: the peer with the lowest download rate cannot obtain all F bits of the file in less than F/dmin seconds.
- • Step3: the total upload capacity of the system is, utotal = us + u1 + … + uN.

- – The system must deliver (upload) F bits to each of the N peers.
- – This cannot be done at a rate faster than utotal.
- – So, the minimum distribution time is also at least NF/(us + u1 + … + uN).


- • Finally, the minimum distribution time for P2P


![](<05d9fd5d99ac557f1dfa74c097f7c1cbc9b34be0_page_6_images/imageFile2.png>)

29-01-2020 Dr. Manas Khatua 6

