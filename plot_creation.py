import streamlit as st
import plotly.express as px

def create_plot(df, plots_config):
    for plot_key in plots_config.keys():
        selected_plot = plot_key
        title = selected_plot

        x_column = st.sidebar.selectbox(f"{title} X-axis", df.columns, index=df.columns.get_loc(plots_config[selected_plot]['x']), key=f'{selected_plot}_x_key')
        y_column = st.sidebar.selectbox(f"{title} Y-axis", df.columns, index=df.columns.get_loc(plots_config[selected_plot]['y']), key=f'{selected_plot}_y_key')
        color_column = st.sidebar.selectbox(f"{title} Color", df.columns, key=f'{selected_plot}_color_key')
        color_palette = st.sidebar.selectbox(f"{title} Color Palette", ["Viridis", "Plasma", "Inferno", "Magma", "Cividis", "Plotly"], key=f'{selected_plot}_palette_key')
        plot_type = st.sidebar.selectbox(f"{title} Plot Type", ["Scatter Plot", "Line Plot", "Box Plot", "Violin Plot"], index=plots_config[selected_plot]['plot_type'], key=f'{selected_plot}_plot_type_key')

        # Update plot configuration
        plots_config[selected_plot]['x'] = x_column
        plots_config[selected_plot]['y'] = y_column
        plots_config[selected_plot]['plot_type'] = plot_type

        fig = None
        if plot_type == "Scatter Plot":
            fig = px.scatter(df, x=x_column, y=y_column, color=color_column, color_continuous_scale=color_palette, title=title)
        elif plot_type == "Line Plot":
            fig = px.line(df, x=x_column, y=y_column, color=color_column, title=title)
        elif plot_type == "Box Plot":
            fig = px.box(df, x=x_column, y=y_column, color=color_column, title=title)
        elif plot_type == "Violin Plot":
            fig = px.violin(df, x=x_column, y=y_column, color=color_column, title=title)

        if fig:
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                width=1000,
                height=800
            )
            st.plotly_chart(fig)
        else:
            st.info(f"Please select values for the {title} X and Y axis.")
