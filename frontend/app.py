import streamlit as st
import requests
import json
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="AutoNet Config Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_ENDPOINT = f"{API_BASE_URL}/api/configs/generate/"

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_url = st.text_input("API Base URL", value=API_BASE_URL)
    use_nlp = st.checkbox("Enable NLP (OpenAI)", value=False, help="Use advanced NLP parsing instead of regex")
    st.markdown("---")
    st.markdown("### 📚 Quick Help")
    st.info("""
    **How to use:**
    1. Enter a network command
    2. Click 'Generate Config'
    3. Review the output
    4. Export or Validate
    5. View history
    """)

# Main Header
st.markdown("""
    <div class="main-header">
        <h1>🌐 AutoNet Config Dashboard</h1>
        <p>AI-Powered Network Configuration Generator</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔧 Generate Config", "📋 History", "📊 Analytics", "ℹ️ About"])

# ============================================================================
# TAB 1: Generate Configuration
# ============================================================================
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Enter Network Command")
        command = st.text_area(
            "Natural Language Command:",
            placeholder="Example: Create VLAN for Sales, IP range 10.0.0.0/24",
            height=100,
            label_visibility="collapsed"
        )
    
    with col2:
        st.subheader("Options")
        config_type = st.selectbox(
            "Config Type:",
            ["vlan", "firewall", "routing", "access-list"],
            help="Type of network configuration"
        )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        generate_btn = st.button("🚀 Generate Config", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    with col3:
        st.write("")
    
    if clear_btn:
        st.rerun()
    
    # Generate Configuration
    if generate_btn:
        if not command.strip():
            st.error("❌ Please enter a network command first!")
        else:
            with st.spinner("⏳ Generating configuration..."):
                try:
                    # Call Django API
                    payload = {
                        "command": command,
                        "use_nlp": use_nlp
                    }
                    
                    response = requests.post(API_ENDPOINT, json=payload, timeout=10)
                    
                    if response.status_code == 201:
                        data = response.json()
                        
                        # Store in session for later use
                        st.session_state.last_config = data
                        st.session_state.last_command = command
                        
                        # Display success
                        st.markdown("""
                            <div class="success-box">
                            ✅ <b>Configuration generated successfully!</b>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Display config details
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Config ID", data.get('id', 'N/A'))
                            st.metric("Status", data.get('status', 'N/A').upper())
                        
                        with col2:
                            st.metric("Config Type", data.get('config_type', 'N/A').upper())
                            st.metric("Validation", "✅ Valid" if data.get('is_valid') else "❌ Invalid")
                        
                        st.markdown("---")
                        
                        # Display Generated Config
                        st.subheader("📄 Generated Configuration")
                        st.code(data.get('config', ''), language="bash")
                        
                        # Validation Errors (if any)
                        if data.get('validation_errors'):
                            st.warning("⚠️ Validation Warnings:")
                            for key, value in data['validation_errors'].items():
                                st.write(f"  • **{key}**: {value}")
                        
                        # Action buttons
                        st.markdown("---")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("💾 Export as .cfg", use_container_width=True):
                                cfg_content = data.get('config', '')
                                st.download_button(
                                    label="⬇️ Download Config",
                                    data=cfg_content,
                                    file_name=f"config_{data['id']}.cfg",
                                    mime="text/plain",
                                    use_container_width=True
                                )
                        
                        with col2:
                            if st.button("✔️ Validate", use_container_width=True):
                                if data.get('is_valid'):
                                    st.success("✅ Configuration is valid!")
                                else:
                                    st.error("❌ Configuration has errors!")
                        
                        with col3:
                            if st.button("🎯 Apply Simulation", use_container_width=True):
                                st.info("🔄 Simulating configuration apply...")
                                st.success("✅ Configuration applied successfully in mock environment!")
                    
                    elif response.status_code == 400:
                        error_data = response.json()
                        st.markdown("""
                            <div class="error-box">
                            ❌ <b>Error generating configuration:</b><br>
                        """, unsafe_allow_html=True)
                        st.error(error_data.get('error', 'Unknown error occurred'))
                    
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        st.error(response.text)
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API. Make sure Django server is running on " + api_url)
                except requests.exceptions.Timeout:
                    st.error("❌ Request timeout. Server took too long to respond.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============================================================================
# TAB 2: Configuration History
# ============================================================================
with tab2:
    st.subheader("📋 Configuration History")
    
    try:
        # Fetch all configs from API
        response = requests.get(f"{api_url}/api/configs/", timeout=10)
        
        if response.status_code == 200:
            configs = response.json()
            
            if isinstance(configs, dict) and 'results' in configs:
                configs = configs['results']
            
            if configs:
                # Display as table
                st.info(f"📌 Total configurations: {len(configs)}")
                
                for config in configs[:10]:  # Show last 10
                    with st.expander(f"Config #{config['id']} - {config['config_type'].upper()} - {config['status']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Status:** {config['status']}")
                            st.write(f"**Type:** {config['config_type']}")
                            st.write(f"**Created:** {config['created_at'][:10]}")
                        
                        with col2:
                            st.write(f"**Command:** {config['natural_language_input'][:50]}...")
                            if config.get('file_path'):
                                st.write(f"**File:** {config['file_path']}")
                        
                        st.write("---")
                        st.write("**Generated Config:**")
                        st.code(config['generated_config'], language="bash")
            else:
                st.info("📭 No configurations yet. Generate one in the 'Generate Config' tab!")
        else:
            st.error("Failed to fetch history")
    
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ Cannot connect to backend API")
    except Exception as e:
        st.error(f"Error fetching history: {str(e)}")

# ============================================================================
# TAB 3: Analytics
# ============================================================================
with tab3:
    st.subheader("📊 Analytics & Statistics")
    
    try:
        response = requests.get(f"{api_url}/api/configs/", timeout=10)
        
        if response.status_code == 200:
            configs = response.json()
            
            if isinstance(configs, dict) and 'results' in configs:
                configs = configs['results']
            
            if configs:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Configs", len(configs))
                
                with col2:
                    validated = len([c for c in configs if c['status'] == 'validated'])
                    st.metric("Validated", validated)
                
                with col3:
                    applied = len([c for c in configs if c['status'] == 'applied'])
                    st.metric("Applied", applied)
                
                st.markdown("---")
                
                # Config types distribution
                st.subheader("Configuration Types")
                config_types = {}
                for config in configs:
                    config_type = config['config_type']
                    config_types[config_type] = config_types.get(config_type, 0) + 1
                
                st.bar_chart(config_types)
                
                # Status distribution
                st.subheader("Status Distribution")
                statuses = {}
                for config in configs:
                    status = config['status']
                    statuses[status] = statuses.get(status, 0) + 1
                
                st.pie_chart(statuses)
            else:
                st.info("No data available yet")
        else:
            st.error("Failed to fetch analytics")
    
    except Exception as e:
        st.warning(f"⚠️ {str(e)}")

# ============================================================================
# TAB 4: About
# ============================================================================
with tab4:
    st.subheader("ℹ️ About AutoNet Config")
    
    st.markdown("""
    ## 🌐 AutoNet Config Dashboard
    
    ### What is AutoNet Config?
    AutoNet Config is an **AI-powered network configuration generator** that translates 
    natural language requirements into validated network device configuration scripts.
    
    ### Features
    - 📝 **Natural Language Input** - Describe your network needs in plain English
    - ⚡ **Instant Generation** - Get configs in seconds
    - ✅ **Validation** - Automatic syntax checking
    - 💾 **Export** - Download as .cfg files
    - 🎯 **Simulation** - Test in mock environment
    - 📊 **History** - Track all generated configurations
    - 🤖 **NLP Support** - Optional OpenAI integration for advanced parsing
    
    ### Architecture
    - **Backend:** Django 4.2 with Django REST Framework
    - **Frontend:** Streamlit (Python)
    - **Database:** SQLite (development) / PostgreSQL (production)
    - **Parser:** Regex-based (MVP) + NLP-ready (OpenAI)
    - **Validator:** Built-in syntax validation
    
    ### Supported Config Types
    - 🔹 VLAN Configuration
    - 🔹 Firewall Rules
    - 🔹 Routing Configuration
    - 🔹 Access Lists
    
    ### Example Usage
    **Input:**
    ```
    Create VLAN for Sales, IP range 10.0.0.0/24
    ```
    
    **Output:**
    ```
    vlan 10
     name Sales
    interface vlan 10
     ip address 10.0.0.1 255.255.255.0
     no shutdown
    ```
    
    ### Next Steps
    - [ ] Implement full NLP with OpenAI
    - [ ] Add Netmiko integration
    - [ ] Support multiple device types
    - [ ] Add user authentication
    - [ ] Mobile app support
    
    ### Resources
    - 📖 [Django Documentation](https://docs.djangoproject.com/)
    - 📖 [Streamlit Documentation](https://docs.streamlit.io/)
    - 🐍 [Python.org](https://www.python.org/)
    - 🤖 [OpenAI API](https://platform.openai.com/)
    
    ---
    
    **Made with ❤️ using Python**
    """)
    
    st.markdown("---")
    st.markdown("""
    ### Support
    For issues or questions, visit:
    [GitHub Repository](https://github.com/suhan-iii/AI-Assistant-for-Network-Configuration-)
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px;">
    <p>🌐 AutoNet Config | AI-Powered Network Configuration Generator</p>
    <p>Made with Streamlit | Powered by Django</p>
    </div>
""", unsafe_allow_html=True)
