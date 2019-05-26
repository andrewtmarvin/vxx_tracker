# This file and gmailcreds.json no longer needed


# from __future__ import print_function
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
#
# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
#
#
# def main():
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'gmailcreds.json', SCOPES)
#             creds = flow.run_local_server()
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('gmail', 'v1', credentials=creds)
#
#     # Call the Gmail API
#     results = service.users().messages().list(userId='me').execute()
#     messages = results.get('messages', [])
#     msg = messages[0]
#
#     if not msg:
#         print('No messages found.')
#     else:
#         msg = service.users().messages().get(userId='me', id=msg['id']).execute()
#         return msg['snippet'][17:24].replace(" ", "") # Grabs code from email for two factor auth
#         # return msg['snippet'][141:-54]  # Grabs the security check code from the email in old method
#
#
# if __name__ == '__main__':
#     main()
