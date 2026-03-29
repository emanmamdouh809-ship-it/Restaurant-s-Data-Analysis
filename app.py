import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Restaurant Sales Analysis',layout='wide')

df = pd.read_csv('cleaned_restaurant_sales_data.csv',index_col=0)

df['order_date'] = pd.to_datetime(df['order_date'])

# Kpis Design 
st.markdown("""
<style>

.kpi-card {
    background-color: rgba(200, 200, 200, 0.15);  
    border: 1px solid rgba(150, 150, 150, 0.4);  
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
}

.kpi-title {font-size: 16px; color: #555; font-weight: bold;}

.kpi-value { font-size: 16px; font-weight: bold; color: black;}

</style>
""", unsafe_allow_html=True)

# Tabs Design

st.markdown("""
<style>

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(200, 200, 200, 0.2);
    border-radius: 10px;
    padding: 10px 20px;
    font-family: 'Poppins', sans-serif;
    font-weight: bold;
    color: #555;
    border: 1px solid transparent;
    transition: 0.3s;}

.stTabs [data-baseweb="tab"]:hover {background-color: rgba(180, 180, 180, 0.3);}

.stTabs [aria-selected="true"] { background-color: white;
    color: black;
    font-weight: bold;
    border: 1px solid rgba(150,150,150,0.4);
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);}

</style>
""", unsafe_allow_html=True)

# background color
st.markdown(
    """
    <style>
    .stApp { background-color: #FEEBE7; }
    </style>
    """,
    unsafe_allow_html=True   )

#Sidebar
with st.sidebar:

   # Date range filter
    start_default = df['order_date'].min().date()
    end_default   = df['order_date'].max().date()

    dates = st.sidebar.date_input(
    "Select Date Range",
    value=(start_default, end_default),
    min_value=start_default,
    max_value=end_default)

# for solve the error when user select only one date instead of range

    if isinstance(dates, tuple) and len(dates) == 2:
        
            start_date, end_date = dates
    elif isinstance(dates, tuple) and len(dates) == 1:
        
            start_date = dates[0]
            end_date = end_default 
            st.info("")
    else:
        
            start_date = dates
            end_date = end_default
            st.info("")
    
    start_date_ts = pd.to_datetime(start_date)
    end_date_ts   = pd.to_datetime(end_date)

    st.title("Restaurant Sales Analysis")
    st.image("logo.png", width=250)

    # page selection
    page = st.sidebar.radio("Select page", ["Main Dashboard", "Analysis", "Insights and Recommendations"])
    
    # Filters
    st.title("Filters")
    Category_Filter = st.multiselect("Select Category", options=df['category'].unique(), default=df['category'].unique())
    Item_Filter = st.multiselect("Select Item", options=df['item'].unique(), default=df['item'].unique())
    Payment_Filter = st.multiselect("Select Payment Method", options=df['payment_method'].unique(), default=df['payment_method'].unique())
    Price_filter=st.slider('Price Range',int(df['price'].min()),int(df['price'].max()),(int(df['price'].min()),int(df['price'].max())))

    Filtered_df = df[(df['order_date'] >= start_date_ts) &
    (df['order_date'] <= end_date_ts) &
    (df['category'].isin(Category_Filter)) &
    (df['item'].isin(Item_Filter)) &
    (df['payment_method'].isin(Payment_Filter)) &
    (df['price'].between(Price_filter[0], Price_filter[1]))]



# Pages 
# MAIN DASHBOARD
if page == "Main Dashboard":

    st.markdown("<h1 style='color:black; text-decoration: underline;'>Main Dashboard</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Total Revenue</div>
        <div class="kpi-value">${Filtered_df['order_total'].sum():,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    AOV = Filtered_df['order_total'].sum() / Filtered_df['order_id'].nunique()
    col2.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💵 Average Order Value</div>
        <div class="kpi-value">${AOV:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🧾 Total Orders</div>
        <div class="kpi-value">{Filtered_df['order_id'].nunique():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📦 Total Quantity Sold</div>
        <div class="kpi-value">{Filtered_df['quantity'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
  
    col5.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">👥 Number of Customers</div>
        <div class="kpi-value">{Filtered_df['customer_id'].nunique()}</div> 
    </div>
    """, unsafe_allow_html=True)

    customer_orders = Filtered_df.groupby('customer_id')['order_id'].nunique()
    repeat_customers = customer_orders[customer_orders > 1].count()
    total_customers = Filtered_df['customer_id'].nunique()
    repeat_rate = (repeat_customers / total_customers) * 100

    col6.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🔁 Repeat Customer Rate</div>
        <div class="kpi-value">{repeat_rate:.2f}%</div> 
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<h2 style='color:black; '>Dataset Preview</h2>", unsafe_allow_html=True)
   
    Filtered_df_display = Filtered_df.copy()
    Filtered_df_display['order_date'] = Filtered_df_display['order_date'].dt.strftime('%Y-%m-%d')

    st.dataframe(Filtered_df_display)

# ANALYSIS PAGE

elif page == "Analysis":
    st.markdown("<h1 style='color:black; text-decoration: underline;'>Restaurant Sales Analysis</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"])


    
    with tab1:
       
        st.markdown("<h2 style='color:black; '>Univariate analysis</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
       
        with col1:
            
                fig1 = px.histogram(Filtered_df, x='category', title='Distribution of Categories')
                fig1.update_traces(textfont=dict(color='black'))
                fig1.update_layout(
                    paper_bgcolor='rgba(255,255,255,0.8)',   
                    plot_bgcolor='rgba(245,245,245,1)',      

                    xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                    title_font=dict(color='black', size=12),     
                    tickfont=dict(color='black', size=11) ),

                    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                    title_font=dict(color='black', size=12),      
                    tickfont=dict(color='black', size=11) ),
                    margin=dict(l=10, r=10, t=40, b=10),
                    
                    title_font=dict(size=16, color='#333', family="Arial"),  )

                st.plotly_chart(fig1, use_container_width=True)
               
        

        with col2:
                
                fig2 = px.pie(Filtered_df, names='payment_method', title='Distribution of Payment Methods')
                fig2.update_traces(textinfo='percent+label',
                textfont=dict(color='black', size=12))
                fig2.update_layout(
                    paper_bgcolor='rgba(255,255,255,0.8)',
                    plot_bgcolor='rgba(245,245,245,1)',
                    title_font=dict(size=16, color='#333', family="Arial"),
                    margin=dict(l=10, r=10, t=40, b=10),
                    legend=dict(
                        font=dict(color='black', size=11)  
                    )
                        )
                st.plotly_chart(fig2, use_container_width=True)

               
        col3, col4= st.columns(2)
       
        with col3:
            
                fig1 = px.histogram(Filtered_df, x='item', title='Distribution of Items')
                fig1.update_traces(textfont=dict(color='black'))
                fig1.update_layout(
                    paper_bgcolor='rgba(255,255,255,0.8)',   
                    plot_bgcolor='rgba(245,245,245,1)',     

                    xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                    title_font=dict(color='black', size=12),     
                    tickfont=dict(color='black', size=11) ),

                    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                    title_font=dict(color='black', size=12),      
                    tickfont=dict(color='black', size=11) ),
                    margin=dict(l=10, r=10, t=40, b=10),
                    
                    title_font=dict(size=16, color='#333', family="Arial"), )

                st.plotly_chart(fig1, use_container_width=True)
               
        

    with tab2:
     st.markdown("<h2 style='color:black; '>Bivariate analysis</h2>", unsafe_allow_html=True)

     bivariate_tab1, bivariate_tab2, bivariate_tab3= st.tabs([
            "Revenue Analysis", 
            "Categories and items Analysis", 
            "Time Trends" ])

        
    with bivariate_tab1:
        st.markdown("<h3 style='color:black; '>Revenue Analysis</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
                    revenue_by_category = Filtered_df.groupby('category')['order_total'].sum().reset_index().sort_values(by='order_total', ascending=False)
                    fig1 = px.bar(revenue_by_category, x='category', y='order_total', title='Revenue by Category',text='order_total',labels={'order_total':'Revenue'})
                    fig1.update_traces(textfont=dict(color='black'),texttemplate='%{text:,.0f} $')
                    fig1.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      

                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial"),  )
                    st.plotly_chart(fig1, use_container_width=True)

        with col2:
                    top_10_customers_by_rev = Filtered_df.groupby('customer_id')['order_total'].sum().sort_values(ascending=False).head(10).reset_index()
                    fig3 = px.bar(top_10_customers_by_rev, x='order_total', y='customer_id', title='Top 10 Customers by Revenue',orientation='h',text='order_total')
                    fig3.update_traces(textfont=dict(color='black'),texttemplate='%{text:,.0f} $')
                    fig3.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      

                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial") )
                    st.plotly_chart(fig3, use_container_width=True)
        col3= st.columns(1)[0]
        with col3:
                    revenue_by_item = Filtered_df.groupby('item')['order_total'].sum().sort_values(ascending=False).reset_index()
                    fig2 = px.bar(revenue_by_item, x='order_total', y='item', title='Items by Revenue',orientation='h',text='order_total')
                    fig2.update_traces(textfont=dict(color='black'),texttemplate='%{text:,.0f} $')
                    fig2.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      
                        height=700,
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial") )
                    st.plotly_chart(fig2, use_container_width=True)

        
   
       
    with bivariate_tab2:
        st.markdown("<h3 style='color:black; '>Categories and items Analysis</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
                    category_by_quantity = Filtered_df.groupby('category')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=False)
                    fig5 = px.bar(category_by_quantity, x='category', y='quantity', title='Category by Quantity Sold',text='quantity')
                    fig5.update_traces(textfont=dict(color='black'))
                    fig5.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      

                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial"),  )

                    st.plotly_chart(fig5, use_container_width=True)               
    
        with col2:
                    AVG_order_by_category = Filtered_df.groupby('category')['order_total'].mean().reset_index().sort_values(by='order_total', ascending=False)
                    fig6 = px.bar(AVG_order_by_category, x='category', y='order_total', title='Average Order Value by Category',text='order_total',labels={'order_total':'Average Order Value'})
                    fig6.update_traces(textfont=dict(color='black'),texttemplate='%{text:,.2f} $')
                    fig6.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      

                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial"),  )

                    st.plotly_chart(fig6, use_container_width=True)      

        col3 = st.columns(1)[0]

        with col3:
                    item_by_quantity = Filtered_df.groupby('item')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=False)
                    fig7 = px.bar(item_by_quantity, x='quantity', y='item', title='Items by Quantity Sold',text='quantity')
                    fig7.update_traces(textfont=dict(color='black'))
                    fig7.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      
                        height=700,
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial"),  )

                    st.plotly_chart(fig7, use_container_width=True)
        col4 = st.columns(1)[0]
        with col4:
                    top_10_customers_Num_orders = Filtered_df.groupby('customer_id')['order_id'].nunique().sort_values(ascending=False).head(10).reset_index()
                    fig3 = px.bar(top_10_customers_Num_orders, x='order_id', y='customer_id', title='Top 10 Customers by Number of Orders',labels={'order_id':'Number of Orders'},orientation='h',text='order_id')
                    fig3.update_traces(textfont=dict(color='black'),texttemplate='%{text:,.0f}')
                    fig3.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      

                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial") )
                    st.plotly_chart(fig3, use_container_width=True) 

    with bivariate_tab3:
        st.markdown("<h3 style='color:black; '>Time Trends</h3>", unsafe_allow_html=True)

        col1= st.columns(1)[0]

        with col1:
                    Filtered_df['order_date'] = pd.to_datetime(Filtered_df['order_date'])
                    Rev_by_date = (Filtered_df.groupby(pd.Grouper(key='order_date', freq='M'))['order_total'].sum().reset_index())
                    fig8 = px.line(Rev_by_date, x='order_date', y='order_total', title='Revenue Over Time',labels={'order_date':'Date', 'order_total':'Revenue'})
                    fig8.update_traces(textfont=dict(color='black'))
                    fig8.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      

                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial"),  )

                    st.plotly_chart(fig8, use_container_width=True) 

        col2= st.columns(1)[0]

        with col2:
                    Rev_by_date['growth_rate'] = Rev_by_date['order_total'].pct_change() * 100
                    fig_growth = px.line(Rev_by_date,x='order_date',y='growth_rate',title='Revenue Growth Rate (%)')
                    fig_growth.update_traces(textfont=dict(color='black'))
                    fig_growth.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.8)',   
                        plot_bgcolor='rgba(245,245,245,1)',      

                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),     
                        tickfont=dict(color='black', size=11) ),

                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                        title_font=dict(color='black', size=12),      
                        tickfont=dict(color='black', size=11) ),
                        margin=dict(l=10, r=10, t=40, b=10),
                        
                        title_font=dict(size=16, color='#333', family="Arial"),  )

                    st.plotly_chart(fig_growth, use_container_width=True)           
       
    with tab3:
        st.markdown("<h2 style='color:black; '>Multivariate analysis</h2>", unsafe_allow_html=True)
        
        col1= st.columns(1)[0]
        with col1:            
 
                rev_cat_time = (Filtered_df.groupby([pd.Grouper(key='order_date', freq='M'), 'category'])['order_total'].sum().reset_index())
                fig9 = px.line(rev_cat_time,x='order_date',y='order_total',color='category',title='Revenue by Category Over Time')
                fig9.update_traces(textfont=dict(color='black'))
                fig9.update_layout(
                    paper_bgcolor='rgba(255,255,255,0.8)',   
                    plot_bgcolor='rgba(245,245,245,1)',      
                    legend=dict(font=dict(color='black', size=12),title_font=dict(color='black', size=12)),
                    xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                    title_font=dict(color='black', size=12),
                    tickfont=dict(color='black', size=11) ),

                    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                    title_font=dict(color='black', size=12),      
                    tickfont=dict(color='black', size=11) ),
                    margin=dict(l=10, r=10, t=40, b=10),
                    
                    title_font=dict(size=16, color='#333', family="Arial"),)  
                st.plotly_chart(fig9, use_container_width=True)

        col2= st.columns(1)[0]
        with col2:
     
                Filtered_df['order_date'] = pd.to_datetime(Filtered_df['order_date'])
                Filtered_df['day'] = Filtered_df['order_date'].dt.day_name()
                heatmap_cat_day = (Filtered_df.groupby(['day', 'category']).size().reset_index(name='orders'))
                fig11 = px.density_heatmap(heatmap_cat_day,x='category', y='day',z='orders',title='Orders by Category and Day',
                    category_orders={ 'day': ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']})
                fig11.update_coloraxes(colorbar=dict(title=dict(text='Orders',font=dict(color='black'))), colorbar_tickfont_color='black')
                fig11.update_layout(
                    paper_bgcolor='rgba(255,255,255,0.8)',   
                    plot_bgcolor='rgba(245,245,245,1)',      
                    xaxis=dict(
                        title='Category',
                        title_font=dict(color='black', size=12),
                        tickfont=dict(color='black', size=11) ),

                    yaxis=dict(
                        title='Day of Week',
                        title_font=dict(color='black', size=12),
                        tickfont=dict(color='black', size=11)  ),

                    margin=dict(l=10, r=10, t=40, b=10),
                    title_font=dict(size=16, color='#333', family="Arial")   )
                st.plotly_chart(fig11, use_container_width=True)

        col3= st.columns(1)[0]
        with col3:
                
                top10_customers = (Filtered_df.groupby('customer_id').agg(total_revenue=('order_total','sum'), order_count=('customer_id','count'))
                    .sort_values('total_revenue', ascending=False).head(10).reset_index())

                df_melted = top10_customers.melt(id_vars='customer_id', value_vars=['total_revenue','order_count'],var_name='Metric',value_name='Value' )

                fig = px.bar(df_melted,x='customer_id',y='Value',color='Metric',barmode='group',text='Value',title='Top 10 Customers by Revenue vs Number of Orders',
                    labels={'customer_id':'Customer', 'Value':'Value'},)
               
                fig.update_traces(texttemplate='%{text:.2f}',textfont=dict(color='black'), textposition='outside')
                fig.update_layout(paper_bgcolor='rgba(255,255,255,0.8)',plot_bgcolor='rgba(245,245,245,1)',title_font=dict(color='black', size=16),
                    legend=dict(font=dict(color='black', size=12),title_font=dict(color='black', size=12)),

                    xaxis=dict( title='Customer',
                    tickangle=-45,
                    title_font=dict(color='black', size=12),
                    tickfont=dict(color='black', size=11) ),

                    yaxis=dict(title='Value',title_font=dict(color='black', size=12),tickfont=dict(color='black', size=11) ))

                st.plotly_chart(fig, use_container_width=True)                    
else :
    st.markdown("<h1 style='color:black; text-decoration: underline;'>Insights and Recommendations</h1>", unsafe_allow_html=True)
    
    st.markdown("""
                <style>
                .box {
                    background-color: rgba(245,245,245,0.9);
                    padding: 20px;
                    border-radius: 15px;
                    margin-bottom: 15px;
                    border: 1px solid #ddd;
                }
                .title {
                    font-size: 20px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                .text {
                    font-size: 15px;
                    color: #444;
                    line-height: 1.8;
                }
                </style>
                """, unsafe_allow_html=True)

    col0 = st.columns(1)[0]
    with col0:
    
                    
                    st.markdown("""
                    <div class="box">
                        <div class="title">💡 Main Project Question:</div>
                        <div class="text">
                            What are the key factors driving revenue and customer behavior in the restaurant, and how can the restaurant optimize sales and customer retention?
                        </div>
                    </div>
                    
                    <div class="box">
                        <div class="title">📝 Sub-Questions:</div>
                        <div class="text">
                            👤 Who are the top customers?<br><br>
                            🛒 Which product categories generate the most revenue and which need improvement?<br><br>
                            💰 What is the average order value?<br><br>
                            📈 Are there patterns in sales over time (daily, weekly, or monthly trends)?<br><br>
                            💳 How does the payment method affect sales and customer behavior?<br><br>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    

    col1, col2 = st.columns(2)
    with col1:
                    st.markdown("""
                    <div class="box">
                        <div class="title">📊 Insights</div>
                        <div class="text">
                        1. The repeat customer rate is 100%, indicating strong customer loyalty and satisfaction.<br><br>
                        2. Top items by quantity sold: <b>Pasta Alfredo</b> (Main Dish) and <b>Side Salad</b> (Side Dishes).<br><br>
                        3. Top items by revenue: <b>Grilled Chicken</b> and <b>Pasta Alfredo</b> (Main Dishes).<br><br>
                        4. Top category by quantity sold, revenue and Average Order Value: <b>Main Dishes</b>.<br><br>
                        5. April is the top revenue month, indicating higher demand during this period.<br><br>
                        6. Growth rate showing unstable performance.<br><br>
                        7. Order patterns vary by both day of the week and category, with noticeable peaks such as high demand for Side Dishes on Sunday and Starters on Saturday.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with col2:
                    st.markdown("""
                    <div class="box">
                        <div class="title">💡Business Recommendations</div>
                        <div class="text">
                        1. Increase <b>average order value</b> through bundles.<br><br> 
                        2 Target top repeat customers with personalized offers and promotions, and plan marketing campaigns to attract new customers or explore new segments.<br><br>
                        3. <b>High-order, low-revenue customers</b> → target with special offers to increase average order value.<br><br>
                        4. <b>High-revenue, low-frequency customers</b> → use personalized campaigns to increase order frequency.<br><br>
                        5. Leverage high customer loyalty with loyalty programs or special offers.<br><br>
                        6. Focus on promoting <b>Main Dishes</b> as they drive the highest revenue and demandand, and introduce new items in the Main Dishes category.<br><br>
                        7. Boost marketing campaigns before and during April to maximize sales, Ensure sufficient inventory and resources to meet the increased demand.<br><br>
                        8. Try different products, reach more customers and prepare strategies to manage periods of low growth.<br><br>
                        9. Adjust promotions, inventory, and staffing based on daily demand patterns.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
