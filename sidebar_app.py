import streamlit as st

def show_sidebar(cookie_manager):
    with st.sidebar:
        user = st.session_state.get('user_data', {"nama": "User", "email": ""})
        # Pastikan nama tidak None, jika None ganti jadi 'Member'
        nama_u = user.get('nama') if user.get('nama') else "Member"
        email_u = user.get('email') if user.get('email') else ""
        
        inisial = nama_u[0].upper() if nama_u else "V"

        # Desain Profil
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px; background-color: #1e293b; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px;">
                <div style="background-color: #fbbf24; color: #1e293b; width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px; font-size: 18px;">{inisial}</div>
                <div style="overflow: hidden;">
                    <p style="margin: 0; color: white; font-weight: bold; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{nama_u}</p>
                    <p style="margin: 0; color: #94a3b8; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{email_u}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Menu Navigasi
        if st.button("🏠 Dashboard Utama", use_container_width=True):
            st.session_state.page = "dashboard"; st.rerun()
            
        if st.button("⚙️ Pengaturan Profil", use_container_width=True):
            st.session_state.page = "settings"; st.rerun()

        st.write("---")
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            cookie_manager.delete("vip_user_email")
            cookie_manager.delete("vip_user_nama")
            st.session_state.authenticated = False
            st.rerun()
            
