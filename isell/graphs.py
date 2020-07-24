from graphos.renderers import gchart
from graphos.sources.model import SimpleDataSource

def get_chart(data,type):

    data_source=[]
    data_source.append(['Date',type])
    if(len(data) == 0):
        data_source.append(['No Data', 0])
    for k,v in data.items():
        # date_=""
        # date_=datetime.datetime.strptime(data.index.values[i].astype(str),'%Y-%m-%dT00:00:00.000000000')
        # date_=datetime.datetime.strftime(date_,'%d %b %Y')
        data_source.append([k,v])

    options1={'title': type
        ,'series': [ { 'color': '#000080' }],
              }

    #       <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    # <script type="text/javascript">
    #     google.load("visualization", "1", {packages:["corechart"]});
    # </script>                               {{ products_chart.as_html }}
                                            
    chart_name = gchart.LineChart(SimpleDataSource(data=data_source), options=options1,
                                  html_id=type, width="100%")

    return chart_name
