# 12.8.1 Encrypted pools

For more information about how to open the Create Pool window, see Chapter 6, “Storage pools” on page 191. After encryption is enabled, any new pool is created by default as encrypted, as shown in Figure 12-69.

![](<55e1134179961fa68c5245122f44e0e4d88f1c0d203591c788ec8f8d6531ef93_images/imageFile1.png>)

Create Pool

Name:

Poolo

Encryption:

Enable

Data reduction:

Enable

Cancel

Create

Figure 12-69 Create Pool window basic

You can click Create to create an encrypted pool. All storage that is added to this pool is encrypted.

You can customize the Pools view in the management GUI to show pool encryption status. Click Pools → Pools , and then, click Actions → Customize Columns → Encryption , as shown in Figure 12-70.

![](<55e1134179961fa68c5245122f44e0e4d88f1c0d203591c788ec8f8d6531ef93_images/imageFile2.png>)

Dashboard

Create

Actions

Deteult

View All Throttles ,

Data Il"

Monitoring

Name

Encryption

Custornize Columns

Namne

Poolo

0 bytes

5.45 TiB (096)

Pools

State

Capacity

Volumes

Compression Savings

Deduplication Savings

Hosts

Savings

Extent Size

Copy Services

Free Physical Capacity

Accoss

Estimated Comnpression Savings

Estimated Compression Savings %

Settings

Estimated Thin savings

Estimated Thin Savings

Encryption

Site

Data Reduction

Restore Default View

Figure 12-70 Pool encryption state

If you create an unencrypted pool but you add only encrypted arrays or self-encrypting MDisks to the pool, the pool is reported as encrypted because all extents in the pool are encrypted. The pool reverts to the unencrypted state if you add an unencrypted array or MDisk.

