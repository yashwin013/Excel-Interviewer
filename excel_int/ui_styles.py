
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

    /* Chat Bubble Styles */
    .stChatMessage {
        background: transparent;
        border: none;
        box-shadow: none;
        padding: 0.5rem 0;
    }
    .stChatMessage p {
        text-align: left;
        color: #e0e0e0 !important;
    }
    [data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) p {
        color: #cddcff !important;
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
    
    /* --- NEW: Difficulty Button Styles --- */
    div[data-testid="stHorizontalBlock"] .stButton button {
        width: 100%;
        padding: 1.25rem;
        font-size: 1.1rem;
        font-weight: 700;
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    div[data-testid="stHorizontalBlock"] .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    /* Unique colors for each button */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) .stButton button { background-color: #28a745; border-color: #28a745;}
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton button { background-color: #007bff; border-color: #007bff;}
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) .stButton button { background-color: #dc3545; border-color: #dc3545;}

</style>
"""