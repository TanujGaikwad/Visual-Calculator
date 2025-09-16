import streamlit as st
import math

st.markdown("""
    <style>
    button[kind="secondary"] div[data-testid="stMarkdownContainer"] p,
    button[kind="secondary"] span,
    .stButton > button {
        font-size: 1.25rem !important;
    }
    </style>
""", unsafe_allow_html=True)


st.title("Calculator")

if "expression" not in st.session_state:
    st.session_state.expression = ""

result = 0

def button_click(label):
    ops = {
        "ADD": "+",
        "SUBTRACT": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
        "MOD": "%"
    }
    # Track if last action was '='
    if "last_was_equal" not in st.session_state:
        st.session_state.last_was_equal = False

    if label == "=":
        expr = st.session_state.expression
        try:
            result = float(eval(expr))
            st.session_state.expression = str(result)
        except Exception:
            st.session_state.expression = "Error"
        st.session_state.last_was_equal = True
    elif label == "C":
        st.session_state.expression = ""
        st.session_state.last_was_equal = False
    elif label == "SQRT":
        try:
            value = float(st.session_state.expression)
            st.session_state.expression = str(math.sqrt(value))
        except Exception:
            st.session_state.expression = "Error"
        st.session_state.last_was_equal = False
    elif label == "SQUARE":
        try:
            value = float(st.session_state.expression)
            st.session_state.expression = str(value ** 2)
        except Exception:
            st.session_state.expression = "Error"
        st.session_state.last_was_equal = False
    else:
        # If last action was '=', start new input
        if st.session_state.last_was_equal:
            st.session_state.expression = ""
            st.session_state.last_was_equal = False
        elif label == "FUNNY":
            st.session_state.expression = "8008135"
            st.session_state.last_was_equal = False
        else:
            # If last action was '=', start new input
            if st.session_state.last_was_equal:
                st.session_state.expression = ""
                st.session_state.last_was_equal = False
            st.session_state.expression += ops.get(label, label)



# Callback to evaluate expression on input change (Enter or blur)
def evaluate_expression():
    expr = st.session_state.display
    # Only allow valid calculator characters
    valid_chars = set("0123456789.+-*/%")
    filtered = ''.join([c for c in expr if c in valid_chars])
    # If last action was '=', clear for new input
    if "last_was_equal" in st.session_state and st.session_state.last_was_equal:
        st.session_state.expression = ''
        st.session_state.display = filtered[-1] if filtered else ''
        st.session_state.last_was_equal = False
        return
    st.session_state.display = filtered
    st.session_state.expression = filtered
    if filtered:
        try:
            result = float(eval(filtered))
            st.session_state.expression = str(result)
            st.session_state.display = str(result)
        except Exception:
            pass  # Don't update on partial/invalid input

# Add a text input to capture keyboard events (including numpad)
user_input = st.text_input(
    "Input",
    st.session_state.expression,
    key="display",
    disabled=False,
    on_change=evaluate_expression
)

# Use words for operations
buttons = [
    ['7', '8', '9', 'DIVIDE'],
    ['4', '5', '6', 'MULTIPLY'],
    ['1', '2', '3', 'SUBTRACT'],
    ['=', '0', '.', 'ADD'],
    ['C', 'SQRT', 'SQUARE', 'MOD', 'FUNNY']
]

for row in buttons:
    cols = st.columns(len(row), gap="small")
    for i, label in enumerate(row):
        cols[i].button(label, on_click=button_click, args=(label,), use_container_width=True)

