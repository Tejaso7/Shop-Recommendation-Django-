# myapp/views.py
import csv
import folium as fo
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm , SearchForm
from .models import MyModel

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Check if the file is a CSV file
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file.')
                return redirect('upload_csv')

            # Read and process the CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    MyModel.objects.create(
                        name=row['name'],
                        location=row['location'],
                        items=row['items'],
                        lat_long=row['lat_long'],
                        full_details=row['full_details']
                    )
                messages.success(request, 'CSV file has been uploaded successfully.')
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {e}')
                return redirect('upload_csv')

            return redirect('upload_csv')
    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})


def search(request):
    form = SearchForm()
    results = []
    if 'Food' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['Food']
            results = MyModel.objects.filter(items__icontains=query) | \
                      MyModel.objects.filter(full_details__icontains=query)
            maps=[]
            x = []
            
            for result in results:
                try:
                    lat, long = map(float, result.lat_long.split(','))
                    folium_map = fo.Map(location=[lat, long], zoom_start=15)
                    fo.Marker(location=[lat, long], popup=result.name, icon=fo.Icon(color='blue')).add_to(folium_map)
                    maps.append(folium_map._repr_html_())
                   
                    x_items = result.items.split(",")
                    for x_item in x_items:
                        x_name, x_price = x_item.split(":")
                        x.append((x_name.strip(), x_price.strip()))
                except Exception as e:
                    maps.append(" ♻️ Unable to load map")
                    x.append("Items are not found!")                
            return render(request, 'search.html', {'form': form, 'results': zip(results, maps), 'x':x })
                    
        
    return render(request, 'search.html', {'form': form, 'results': results })
        

def home(request):
    return render(request,'home.html')