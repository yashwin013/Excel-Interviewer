# ui_styles.py

css = """
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* General Styles & Aurora Background */
    .stApp {
        background-color: #0e1117;
        background-image: 
            radial-gradient(at 20% 20%, hsla(210, 80%, 30%, 0.3) 0px, transparent 50%),
            radial-gradient(at 80% 20%, hsla(280, 80%, 30%, 0.3) 0px, transparent 50%),
            radial-gradient(at 80% 80%, hsla(340, 80%, 30%, 0.3) 0px, transparent 50%),
            radial-gradient(at 20% 80%, hsla(170, 80%, 30%, 0.3) 0px, transparent 50%);
        background-attachment: fixed;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* Header Styles */
    h1, h3 {
        text-align: center;
        color: #ffffff;
    }
    
    p {
        text-align: center;
        color: #a0a0a0;
    }


    /* Chat Bubble Styles - REMOVED the blocky container */
    .stChatMessage {
        background: transparent;
        border: none;
        box-shadow: none;
        padding: 0.5rem 0; /* Adjusted padding for a cleaner look */
    }

    /* Make text inside bubbles left-aligned */
    .stChatMessage p {
        text-align: left;
        color: #e0e0e0 !important; /* Force light text color */
    }

    /* User message text color */
    [data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) p {
         color: #cddcff !important; /* Slightly different color for user text */
    }


    /* Chat input box */
    [data-testid="stChatInput"] {
        background-color: transparent;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stChatInput"] > div > div > textarea {
        background: rgba(44, 47, 56, 0.7);
        color: #e0e0e0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
</style>
"""