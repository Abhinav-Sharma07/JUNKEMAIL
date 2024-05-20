import streamlit as st
import time
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from streamlit_navigation_bar import st_navbar

# Download nltk resources
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# Load model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Page Layout
st.set_page_config(
    page_title="JUNKEMAIL",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
    
)
navigation_items = ["JUNKEMAIL ","                                                     ", "Made by Abhinav" ]
page=st_navbar(navigation_items)

# Main Content
st.markdown("<h1 style='text-align: center;'>JUNKEMAIL</h1>", unsafe_allow_html=True)

# Message for better results
st.write("Email Test to Check Email is Spam or Not- ")

st.write('''  Estimate your email deliverability rates before you send that next email with the spam score checker by IPQS. Determine if your messages can safely land in a user's inbox, or is likely headed for the dreaded spam folder OR You receiving male is safe or not .
                            Copy and paste the content ''')
input_sms = st.text_area('''Paste the Full Email including headers 

Use our quick spam test to identify which features of your message, SPF or DNS records, or mail server configuration need improvement to deliver directly into the inbox. Detect important issues affecting your inboxing rates with this email deliverability test that predicts email inboxing with a quick email spam check and sender reputation lookup.

Use the email deliverability test by pasting your email content below.''')

if st.button('Predict'):
    # Check if input_sms is empty
    if input_sms.strip() == "":
        st.warning("Please enter a message to predict.")
    else:
        # Show loading spinner
        with st.spinner('Predicting...'):
            time.sleep(3)  # Simulate prediction time
            # 1. Preprocess
            transformed_sms = transform_text(input_sms)
            # 2. Vectorize
            vector_input = tfidf.transform([transformed_sms])
            # 3. Predict
            result = model.predict(vector_input)[0]
            # 4. Display
            if result == 1:
                st.error('''SPAM Warning, Risky Message Detected!
                                7.9 - SPAM - High Risk''')
            else:
                st.success("Not Spam")
st.header("Check Your Spam Score Before Sending")
st.write('''  Since every major mail service provider uses spam filters to some extent, it is considered a best practice to scan your email's subject and message content before sending to your marketing lists. Checking the spam score based on the email content, sender ID, SPF records, DNS settings, IP blacklisting, domain reputation, domain keys, DKIM, and PTR records is a great way to estimate deliverability and avoid the spam folder. This tool can accurately predict inboxing rates for Gmail, Yahoo, AOL, Hotmail, and most popular mail services worldwide.

This spam test tool will provide recommendations to improve IP and domain reputation and other factors which can limit email deliverability and prevent your messages from reaching the inbox folder. The email deliverability test will identify issues with keywords, content, formatting, and DNS records or mail server configurations. Open rates can also be improved by choosing a friendly subject name. Newsletters and marketing content is especially susceptible to spam filtering, so sending quality content and low risk messages can maintain good quality IP and domain reputations and healthy sender scores. ''')

st.header("Tips for Improving Email Deliverability ")
st.write('''  Sending mail is somewhat of an art these days. Technical factors for the domain and IP address need to be set while also ensuring that the content of the email address fits certain standards to not trigger spam filters. The guide below will briefly touch on the best ways to improve deliverability rates using the results from the email deliverability test.

    SPF Record Setup - SPF records use a DNS TXT record to indicate all allowed hostnames and IP addresses that are authorized to send email on behalf of a domain. This allows mail servers to quickly determine if a sender is spoofing email from your domain, which can happen quite frequently. Learn more and setup your SPF record with this guide from dmarcanalzyer.
    PTR Record Setup - PTR records can also be referred to as reverse DNS records. They are typically set with your hosting company so an IP address can resolve to a specific domain name. Ensuring that your IP address and domain have matching forward and reverse DNS records is a major boost to your sender score. Mail services use the PTR record as a significant spam filter.
    DKIM and Domain Keys - This step can vary by your mail service provider, but most platforms now have 1 click enabling of DKIM and Domain Keys. DKIM prevents email spoofing by allowing the receiver to authenticate the sender of the message with a public DKIM key listed in your domain's DNS records.
    Warm Up Sending IPs - It's a proven practice that slowly warming up sending IP addresses can favorably impact your deliverability rates. Start by only sending 50 emails per day per IP and then doubling that number every 3-5 days. It is also recommended to initially message subscribers that have recently been active on your list, such as clicking or opening previous messages. These measures will protect your sender score at the least, but usually improve it quite a bit.
    IP Reputation - Email received from an IP address associated with spamming or unsolicited email marketing is a red flag for all mail service providers. It is recommended to frequently monitor your IP address reputation in addition to checking before mail drops. If your IP address is listed with any public blacklists online, there is typically a delist process that allows your IP to be removed within 24 hours. We recommend Multi RBL for checking if your server's IP address is blacklisted.
    Validate Emails To Limit Bounces - Email hygiene is important, so the best way to ensure low bounce rates and healthy reputation with the mail service providers is to only include valid email addresses in your lists. Scrubbing invalid and deactivated email accounts can instantly improve your chances for reaching the inbox throughout an entire email marketing campaign. You can directly upload a list of mail addresses for email validation.
    Remove Spam Traps - It's widely accepted that spam traps are a hidden killer of marketing campaigns. These email addresses are used as honeypots by mail service providers to capture unsolicited emails. It's recommended to cleanse spam traps from your marketing lists to avoid reputation issues.
    SpamAssassin Filtering - SpamAssassin is a popular spam filter used as the foundation for most major mail service providers and is typically installed on shared hosting and dedicated server environments by default. As one of the most popular filtering systems, it's important to test against SpamAssassin rules and ensure your SpamAssassin score is under 3.
''')

st.header("How To Test Email Content? ")
st.write('''  Scan your email using the email spam test tool above to identify any potential issues with DNS records or even the message's content or subject line. Validate that your SpamAssassin score is as close to 1 as possible. Take the appropriate steps to solve these issues such as delisting your IP address from blacklists and removing spam traps. If all recommendations by our email spam checker have been completed, then move onto the next step of email validation.

Trusting an email validation service that can verify emails and also identify complainers, spam traps, and emails likely to bounce is crucial to maintaining healthy sender scores. It is strongly recommended to never blindly message a marketing list, even if you directly collected the email addresses yourself. Emails can be deactivated or turned into recycled spam traps due to inactivity, so the risk for older contacting lists greatly increases. If a mail service provider notices a bounce rate over a certain threshold, they will blacklist the sending IP or domain.

It can also be helpful to check if any malicious links are present in your marketing messages. IPQS also offers a free tool to check URLs for malware, which could identify issues with message content. If a mail service provider suspects a link is related to phishing or misleading advertising, it can greatly impact inbox deliverability. ''')

st.header("Email Delivery Test ")
st.write(''' Perform a check email spam score request by pasting your message content into the email deliverability test tool above. Since this tool can identify issues that impact your sending reputation including spam keywords, IP reputation, and domain blacklisting — it will highlight critical issues and warnings that can be resolved to improve reputation. This step is crucial to maximize any company's email marketing process. Most of the major mail service providers follow the same best practices, so the email deliverability test includes email spam score checks that are relevant across all spam filtering services. Fixing any issues discovered by the spam filter testing tool can improve email inboxing rates in as little as a few hours. ''')

st.header("What Are Sender Scores? ")
st.write(''' Sender scores provide an email reputation analysis for all marketing messages sent by your active domains and IP addresses. Mail service providers (MSPs) use this data for blacklisting and routing mail into the inbox, promotions tab, or spam folder. Sender reputation can be affected by bounce rates, quality of content, message frequency, DKIM & PTR records, and similar email hygiene factors. ''')

st.header(" How To Improve Email Sender Scores?")
st.write('''  It can only take a few weeks to greatly improve your sender score and any email deliverability issues. The recommendations above such as scrubbing spam traps and complainers, removing invalid email addresses, ensuring healthy DNS records including PTR, DKIM, rDNS, and SPF will satisfy requirements for all mail service providers. Using the email spam checker to analyze your content can also identify buzz words associated with blacklisted keywords. The email deliverability test will incorporate message content, DNS records, and sender reputation into one easy report to identify any possible inboxing issues.

Using a dedicated IP address for sending is also recommended to avoid overlapping with other senders that may be using more aggressive tactics. As bounce rates greatly lower your sender reputation will quickly improve. At this point it can be easy to maintain these standards with routine email list cleaning and use of our real-time email validation API. ''')

st.header("How To Reduce Email Bounces?")
st.write('''A spam filter testing tool cannot view email bounce rates, so this process must be performed in addition to the recommendations from checking your email spam score using the form above. The best way to ensure low bounce rates is an industry best practice of validating email addresses as soon as they subscribe to your newsletter or contact list. Even legitimate users can make typos which would provide an invalid email address that increases your bounce rate. It's important to repeat validation every 3-6 months to identify deactivated accounts, complainers, and those that have been converted into spam traps. IPQS can detect emails with poor reputation that should be scrubbed from your email marketing lists.  ''')

# Define the custom CSS

css = """
<style>
body {
    background: linear-gradient(135deg, #0000ff, #000080); /* Blue gradient */
    color: white;
    font-family: 'Arial', sans-serif;
}
header, .css-1d391kg {
    background-color: #003366; /* Dark blue background for header */
    color: white;
}
.css-1v3fvcr, .css-1d391kg, .css-1cpxqw2 {
    color: #ffcc00; /* Yellow text for titles */
}
.css-1cpxqw2 {
    font-size: 18px;
    font-weight: bold;
}
.css-1d391kg {
    padding: 10px;
    background-color: #00509e; /* Medium blue background for sidebar */
    border-radius: 10px;
}
.css-15zrgzn {
    color: #ffcc00; /* Yellow sidebar text */
}
.css-1v3fvcr {
    font-size: 18px;
}
.css-1x8cf1d {
    background-color: #ffcc00; /* Yellow button */
    color: black;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
}
.css-1x8cf1d:hover {
    background-color: #e6b800; /* Darker yellow on hover */
}
.css-2hb0pl, .css-10trblm {
    background-color: #003366; /* Dark blue background for select box */
    color: white;
    border: 1px solid #ffcc00; /* Yellow border */
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
}
hr {
    border: 0;
    height: 1px;
    background: #ffcc00;
}
#footer p {
    margin: 0;
}
</style>
"""

# Apply the custom CSS
st.markdown(css, unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <hr>
    <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
        <div id="footer" style="text-align: center; font-size: 0.9rem;">
            <p>Build by Abhinav Sharma ⚡</p>
        </div>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    </div>
    """,
    unsafe_allow_html=True
)

# CSS for mobile responsiveness
st.markdown(
    """
    <style>
        /* Mobile responsiveness */
        @media (max-width: 600px) {
            .stTextArea textarea {
                min-height: 100px !important;
            }
            
            .css-vfskoc {
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
            }
        }       
    </style>
    """,
    unsafe_allow_html=True
)
