import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.title("SIMULADOR DE FRENAGEM")
st.subheader("FÍSICA: CINEMÁTICA E DINÂMICA")

# --- ENTRADA DE PARÂMETROS ---
st.write("### Parâmetros de Entrada")
col1, col2, col3 = st.columns(3)

with col1:
    v_inicial_kmh = st.number_input("Velocidade inicial (km/h):", min_value=1.0, value=80.0, step=1.0)
with col2:
    t_reacao = st.number_input("Tempo de reação (s):", min_value=0.1, value=1.0, step=0.1)
with col3:
    coef_atrito = st.number_input("Coeficiente de atrito:", min_value=0.1, value=0.7, step=0.1)

# Gravidade constante (m/s²)
g = 9.81 

if st.button("SIMULAR"):
    # --- CÁLCULOS FÍSICOS ---
    # 1. Conversão de velocidade
    v_inicial_ms = v_inicial_kmh / 3.6
    
    # 2. Aceleração (desaceleração devido ao atrito)
    # Segunda Lei de Newton: Força de Atrito = massa * aceleração -> mu * normal = m * a -> mu * m * g = m * a -> a = mu * g
    aceleracao = coef_atrito * g 
    
    # 3. Distância de Reação (MRU: S = v * t)
    dist_reacao = v_inicial_ms * t_reacao
    
    # 4. Distância de Frenagem (Equação de Torricelli: v² = v0² - 2*a*deltaS -> deltaS = v0² / 2a)
    dist_frenagem = (v_inicial_ms ** 2) / (2 * aceleracao)
    
    # 5. Tempo de Frenagem (v = v0 - a*t -> t = v0 / a)
    t_frenagem = v_inicial_ms / aceleracao
    
    # 6. Totais
    dist_total = dist_reacao + dist_frenagem
    tempo_total = t_reacao + t_frenagem

    # --- RESULTADOS ---
    st.write("### RESULTADOS")
    r_col1, r_col2, r_col3 = st.columns(3)
    
    with r_col1:
        st.info(f"Distância de reação:\n {dist_reacao:.2f} m")
        st.info(f"Tempo total:\n {tempo_total:.2f} s")
    with r_col2:
        st.error(f"Distância de frenagem:\n {dist_frenagem:.2f} m")
        st.warning(f"Aceleração:\n {-aceleracao:.2f} m/s²")
    with r_col3:
        st.success(f"Distância total:\n {dist_total:.2f} m")

    # --- GRÁFICOS (Matplotlib & Numpy) ---
    st.write("### Gráficos do Movimento")
    
    # Gerando dados para os gráficos
    t_array_reacao = np.linspace(0, t_reacao, 50)
    v_array_reacao = np.full_like(t_array_reacao, v_inicial_ms)
    s_array_reacao = v_inicial_ms * t_array_reacao
    
    t_array_frenagem = np.linspace(0, t_frenagem, 100)
    v_array_frenagem = v_inicial_ms - (aceleracao * t_array_frenagem)
    s_array_frenagem = dist_reacao + (v_inicial_ms * t_array_frenagem) - (0.5 * aceleracao * t_array_frenagem**2)
    
    # Concatenando vetores
    t_total_array = np.concatenate((t_array_reacao, t_array_reacao[-1] + t_array_frenagem))
    v_total_array = np.concatenate((v_array_reacao, v_array_frenagem))
    s_total_array = np.concatenate((s_array_reacao, s_array_frenagem))

    # Plotando
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico de Velocidade x Tempo
    ax1.plot(t_total_array, v_total_array * 3.6, color='blue', linewidth=2)
    ax1.axvline(x=t_reacao, color='red', linestyle='--', label='Início da frenagem')
    ax1.set_title("Velocidade x Tempo")
    ax1.set_xlabel("Tempo (s)")
    ax1.set_ylabel("Velocidade (km/h)")
    ax1.grid(True)
    ax1.legend()

    # Gráfico de Espaço x Tempo
    ax2.plot(t_total_array, s_total_array, color='green', linewidth=2)
    ax2.axvline(x=t_reacao, color='red', linestyle='--', label='Início da frenagem')
    ax2.set_title("Distância Percorrida x Tempo")
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("Distância (m)")
    ax2.grid(True)
    ax2.legend()

    st.pyplot(fig)

    import time

    # --- ANIMAÇÃO SIMPLES ---
    st.write("### Visualização do Movimento")
    
    pista = st.empty()
    status = st.empty()
    
    # Simulando em 100 quadros para fluidez
    passos = 100
    for i in range(passos + 1):
        t_atual = (i / passos) * tempo_total
        
        # Lógica para determinar a posição atual baseada no tempo
        if t_atual <= t_reacao:
            # Fase de reação (MRU)
            posicao_atual = v_inicial_ms * t_atual
            fase = "🟢 Fase de Reação (Velocidade Constante)"
        else:
            # Fase de frenagem (MRUV)
            t_fren = t_atual - t_reacao
            posicao_atual = dist_reacao + (v_inicial_ms * t_fren) - (0.5 * aceleracao * (t_fren ** 2))
            fase = "🔴 Fase de Frenagem (Desacelerando)"
            
        # Calcula a porcentagem percorrida para a barra de progresso
        porcentagem = int((posicao_atual / dist_total) * 100)
        
        # Atualiza os elementos na tela a cada iteração
        pista.progress(porcentagem if porcentagem <= 100 else 100)
        status.markdown(f"**{fase}** | Posição: {posicao_atual:.2f} m | Tempo: {t_atual:.2f} s")
        
        # Pequena pausa para criar o efeito visual de animação
        time.sleep(tempo_total / passos)
        
    status.success(f"🏁 Veículo Parado em {dist_total:.2f} m!")