#! python3
# copy email snippet to the clipboard

# plan: 
# 1) paste the snippet directly onto the email draft
# 2) parse the job folder, analyse and auto-fill the content of the snippet

import sys, pyperclip # pyperclip is external module

TEXT = {'new_job': """Please note that [job] is being uploaded to the server, including [no.] images along with the post-production guideline. Let me know if there is any question. Thanks!""",
        'amend_job': """Please note that there are amendments required, which are being uploaded to the server under the folder [job], including [no.] images along with the feedback pdf. Let me know if there is any question. Thanks!"""}

if len(sys.argv) < 2:
    print('Usage: python3 ihs_email.py [keyphrase] - copy phrase')
    sys.exit()

keyphrase = sys.argv[1]

if keyphrase in TEXT:
    pyperclip.copy(TEXT[keyphrase])
    print('Text for ' + keyphrase + 'copied to the clipboard')
else:
    print('Keyphrase [' + keyphrase + '] not exist!\n')
    print('====================')
    print('Keyphrase includes:')
    
    i = 1
    for k in TEXT.keys():
        print(str(i) + ') ' + k)
        i = i + 1
