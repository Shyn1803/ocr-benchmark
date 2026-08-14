- 3. In the next window, you can choose between IBM SKLM or Gemalto SefeNet KeySecure server types, as shown in Figure 12-42. Select Gemalto SefeNet KeySecure and click Next.

- Figure 12-42 Selecting Gemalto SafeNet KeySecure as key server type

4. Add up to four SafeNet KeySecure servers in the next wizard window, as shown in

- Figure 12-43 on page 638. For each key server, enter the name, IP address and TCP port for KMIP protocol (default value is 5696). Note that server name is only a label, so it does not need to be the real host name of the server.




<table>
  <tr>
    <td>![](<cfde4d42d279e435b0774c1c1862b79234e3863d2b81cc28b881b7f3360ef852_images/imageFile1.png>)</td>
  </tr>
</table>


Although Gemalto SafeNet KeySecure uses an active-active clustered model, IBM Spectrum Virtualize asks for a primary key server. The primary key server represents only the KeySecure server that is used for key create and rekey operations. Therefore, any of the clustered key servers can be selected as the primary.

Selecting a primary key server is beneficial for load balancing. Any four key servers can be used to retrieve the master key.

Chapter 12. Encryption 637

