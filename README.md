# grab_console_url

A Chrome extesion which does the below if you are on a GCP console page.

1. Grabs the URL of the current page and copies it to clipboard. If it's an Google internal Patheon link it converts the URL to a public accessible one, by replacing the domain.
2. Displays the project ID as parsed from the URL, with a button to copy it to clipboard.
3. Displays the shortened URL which is returned from a Cloud Functions call, with a button to copy it to clipboard.

It also provides the source code of the Cloud Functions for the URL shortening.
