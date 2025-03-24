import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="اشكال بيانية")
file = st.file_uploader(label="قم بتحميل الملف", type=["csv", "xlsx", "xls"], accept_multiple_files=False, help="help")
df = pd.DataFrame()
if file:
    if file.type == "text/csv":
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)


    def vision(data):
        st.write("les démonsions de tableau : ", "\n", data.shape, "\n")
        st.write("-*" * 150)
        st.write("les informations de tableau : ", "\n", data.info(), "\n")
        st.write("-*" * 50)
        st.write("les données manquantes : ", "\n", data.isnull().sum(), "\n")
        st.write("-*" * 50)
        st.write("les données dupliquées : ", "\n", data.duplicated().sum(), "\n")
        st.write("-*" * 50)
        st.write("les statistiques descriptives : ", "\n", data.describe(include="all"), "\n")
        st.write("-*" * 50)
        st.write("les valeurs uniques : ", "\n", data.nunique(), "\n")


    vision(df)  # Just call the function, don't st.write() its result since it already contains st.write()

    cols = st.columns(4)
    box2 = cols[0].multiselect(label="drope columns", options=df.columns)
    if box2:
        df = df.drop(columns=box2)
        st.write("Columns after dropping:", df.columns)

        # Partie des graphiques individuels modifiée
        st.subheader("Graphiques individuels")

        # Sélectionner une colonne spécifique à visualiser
        selected_col = st.selectbox("Sélectionnez une colonne à visualiser:", options=df.columns)

        if selected_col and not df.empty:
            # Détecter le type de la colonne
            is_numeric = df[selected_col].dtype != 'object' and df[selected_col].dtype.name != 'category'

            if is_numeric:
                # Options de graphiques pour variables numériques
                graph_type = st.selectbox(
                    "Type de graphique pour variable numérique:",
                    options=["Histogramme", "Box Plot", "KDE (Density)", "Violin Plot", "Cumulative Distribution"],
                    key="num_graph_type"
                )

                if graph_type == "Histogramme":
                    nbins = st.slider("Nombre de bins:", min_value=5, max_value=100, value=20)
                    fig = px.histogram(df, x=selected_col, nbins=nbins,
                                       title=f"Histogramme de {selected_col}")
                    st.plotly_chart(fig)

                elif graph_type == "Box Plot":
                    fig = px.box(df, x=selected_col, title=f"Box Plot de {selected_col}", points='all')
                    st.plotly_chart(fig)

                elif graph_type == "KDE (Density)":
                    fig = px.density_contour(df, x=selected_col, title=f"KDE de {selected_col}")
                    fig.update_traces(contours_coloring="fill", contours_showlabels=True)
                    st.plotly_chart(fig)

                elif graph_type == "Violin Plot":
                    fig = px.violin(df, y=selected_col, box=True, points='all',
                                    title=f"Violin Plot de {selected_col}")
                    st.plotly_chart(fig)

                elif graph_type == "Cumulative Distribution":
                    fig = px.ecdf(df, x=selected_col, title=f"Distribution cumulative de {selected_col}")
                    st.plotly_chart(fig)

            else:
                # Options de graphiques pour variables catégorielles
                graph_type = st.selectbox(
                    "Type de graphique pour variable catégorielle:",
                    options=["Bar Chart", "Pie Chart", "Treemap", "Funnel Chart"],
                    key="cat_graph_type"
                )

                # Limiter les valeurs pour les graphiques circulaires et treemap
                value_counts = df[selected_col].value_counts()

                if graph_type == "Bar Chart":
                    sort_option = st.checkbox("Trier par fréquence", value=True)
                    if sort_option:
                        fig = px.bar(x=value_counts.index, y=value_counts.values,
                                     title=f"Bar Chart de {selected_col}",
                                     labels={'x': selected_col, 'y': 'Count'})
                    else:
                        fig = px.bar(df, x=selected_col, title=f"Bar Chart de {selected_col}")
                    st.plotly_chart(fig)

                elif graph_type == "Pie Chart":
                    # Limiter à 10 catégories max pour la lisibilité des graphiques circulaires
                    if len(value_counts) > 10:
                        st.warning(
                            f"La colonne a {len(value_counts)} valeurs uniques. Affichage limité aux 10 plus fréquentes.")
                        value_counts = value_counts.nlargest(10)

                    fig = px.pie(values=value_counts.values, names=value_counts.index,
                                 title=f"Pie Chart de {selected_col}")
                    st.plotly_chart(fig)

                elif graph_type == "Treemap":
                    # Limiter à 20 catégories max pour la lisibilité
                    if len(value_counts) > 20:
                        st.warning(
                            f"La colonne a {len(value_counts)} valeurs uniques. Affichage limité aux 20 plus fréquentes.")
                        value_counts = value_counts.nlargest(20)

                    fig = px.treemap(
                        names=value_counts.index,
                        values=value_counts.values,
                        title=f"Treemap de {selected_col}"
                    )
                    st.plotly_chart(fig)

                elif graph_type == "Funnel Chart":
                    # Limiter à 10 catégories max pour la lisibilité
                    if len(value_counts) > 10:
                        st.warning(
                            f"La colonne a {len(value_counts)} valeurs uniques. Affichage limité aux 10 plus fréquentes.")
                        value_counts = value_counts.nlargest(10)

                    fig = px.funnel(
                        x=value_counts.values,
                        y=value_counts.index,
                        title=f"Funnel Chart de {selected_col}"
                    )
                    st.plotly_chart(fig)

            # Afficher des statistiques descriptives pour la colonne sélectionnée
            with st.expander("Statistiques descriptives"):
                if is_numeric:
                    st.write(df[selected_col].describe())
                else:
                    st.write(f"Nombre de valeurs uniques: {df[selected_col].nunique()}")
                    st.write("Distribution des valeurs:")
                    st.write(df[selected_col].value_counts())
                    st.write("Distribution en pourcentage:")
                    st.write(df[selected_col].value_counts(normalize=True).mul(100).round(2).astype(str) + ' %')
        # les graphs de deux dim :
        st.title("les graphs de deux dim :")
        ch = st.columns(3)  # Ajout d'une colonne pour le choix du type de graphique
        x_col = ch[0].selectbox(label='X_colonne', options=df.columns)
        y_col = ch[1].selectbox(label='Y_colonne', options=df.columns)

        # Vérifier les types de données pour proposer des graphiques appropriés
        if x_col and y_col and not df.empty:
            x_is_object = df[x_col].dtype == 'object' or df[x_col].dtype.name == 'category'
            y_is_object = df[y_col].dtype == 'object' or df[y_col].dtype.name == 'category'

            # Proposer différents types de graphiques selon les types de données
            if x_is_object and y_is_object:
                # Les deux sont catégorielles - proposer des graphiques adaptés
                graph_type = ch[2].selectbox(
                    label='Type de graphique',
                    options=['Bar Chart', 'Count Plot', 'Heatmap'],
                    key='cat_cat'
                )

                if graph_type == 'Bar Chart':
                    fig = px.bar(df, x=x_col, color=y_col, title=f"Bar Chart of {x_col} by {y_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Count Plot':
                    # Créer un tableau croisé pour le countplot
                    cross_tab = pd.crosstab(df[x_col], df[y_col])
                    fig = px.imshow(cross_tab, text_auto=True, aspect="auto",
                                    title=f"Count Plot of {x_col} vs {y_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Heatmap':
                    # Normaliser le tableau croisé pour avoir des pourcentages
                    cross_tab_norm = pd.crosstab(df[x_col], df[y_col], normalize='index')
                    fig = px.imshow(cross_tab_norm, text_auto='.1%', aspect="auto",
                                    color_continuous_scale='Blues',
                                    title=f"Heatmap of {x_col} vs {y_col} (% par ligne)")
                    st.plotly_chart(fig)

            elif (x_is_object and not y_is_object) or (not x_is_object and y_is_object):
                # Une variable catégorielle et une numérique
                cat_col = x_col if x_is_object else y_col
                num_col = y_col if x_is_object else x_col

                graph_type = ch[2].selectbox(
                    label='Type de graphique',
                    options=['Box Plot', 'Violin Plot', 'Bar Chart', 'Swarm Plot'],
                    key='cat_num'
                )

                if graph_type == 'Box Plot':
                    fig = px.box(df, x=cat_col, y=num_col,
                                 title=f"Box Plot of {num_col} by {cat_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Violin Plot':
                    fig = px.violin(df, x=cat_col, y=num_col, box=True,
                                    title=f"Violin Plot of {num_col} by {cat_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Bar Chart':
                    # Calculer la moyenne par catégorie
                    agg_df = df.groupby(cat_col)[num_col].mean().reset_index()
                    fig = px.bar(agg_df, x=cat_col, y=num_col,
                                 title=f"Average {num_col} by {cat_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Swarm Plot':
                    # Pour un swarm plot, utiliser Plotly Strip Plot comme alternative
                    fig = px.strip(df, x=cat_col, y=num_col,
                                   title=f"Swarm Plot of {num_col} by {cat_col}")
                    st.plotly_chart(fig)

            else:
                # Les deux sont numériques
                graph_type = ch[2].selectbox(
                    label='Type de graphique',
                    options=['Scatter Plot', 'Line Plot', 'Hexbin', 'Density Contour', 'Bubble Chart'],
                    key='num_num'
                )

                if graph_type == 'Scatter Plot':
                    fig = px.scatter(df, x=x_col, y=y_col,
                                     title=f"Scatter Plot of {y_col} vs {x_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Line Plot':
                    # Trier par x pour avoir une ligne cohérente
                    sorted_df = df.sort_values(by=x_col)
                    fig = px.line(sorted_df, x=x_col, y=y_col,
                                  title=f"Line Plot of {y_col} vs {x_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Hexbin':
                    fig = px.density_heatmap(df, x=x_col, y=y_col, nbinsx=20, nbinsy=20,
                                             title=f"Hexbin Plot of {y_col} vs {x_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Density Contour':
                    fig = px.density_contour(df, x=x_col, y=y_col,
                                             title=f"Density Contour of {y_col} vs {x_col}")
                    st.plotly_chart(fig)
                elif graph_type == 'Bubble Chart':
                    # Utiliser une troisième variable numérique pour la taille des bulles si disponible
                    num_cols = df.select_dtypes(include=['float', 'int']).columns
                    if len(num_cols) > 2 and set([x_col, y_col]).issubset(set(num_cols)):
                        size_col = [col for col in num_cols if col not in [x_col, y_col]][0]
                        fig = px.scatter(df, x=x_col, y=y_col, size=size_col,
                                         title=f"Bubble Chart of {y_col} vs {x_col} (size: {size_col})")
                    else:
                        # Si pas de 3ème variable numérique, utiliser une constante
                        fig = px.scatter(df, x=x_col, y=y_col, size_max=15,
                                         title=f"Bubble Chart of {y_col} vs {x_col}")
                    st.plotly_chart(fig)
