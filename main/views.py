# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Calculation
from .forms import CustomRegistrationForm

# --- User Authentication Views ---

def register_view(request):
    if request.user.is_authenticated:
        return redirect('calculator')
        
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('calculator')
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('calculator')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('calculator')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- Main Application Views ---

@login_required
def calculator_view(request):
    context = {}
    if request.method == 'POST':
        # Get data from form, defaulting to 0 if empty
        car_miles = float(request.POST.get('carMiles') or 0)
        car_type = float(request.POST.get('carType') or 0.79)
        public_transport = float(request.POST.get('publicTransport') or 0)
        flights = float(request.POST.get('flights') or 0)
        
        electricity = float(request.POST.get('electricity') or 0)
        natural_gas = float(request.POST.get('naturalGas') or 0)
        renewable = float(request.POST.get('renewable') or 0)

        red_meat = float(request.POST.get('redMeat') or 0)
        poultry = float(request.POST.get('poultry') or 0)
        plant_based = float(request.POST.get('plantBased') or 0)
        food_waste = float(request.POST.get('foodWaste') or 0)
        local_food = float(request.POST.get('localFood') or 0)
        
        clothing = float(request.POST.get('clothing') or 0)
        deliveries = float(request.POST.get('deliveries') or 0)
        electronics = float(request.POST.get('electronics') or 0)
        recycling = float(request.POST.get('recycling') or 0)
        
        # Calculations
        transport_total = (car_miles * car_type) + (public_transport * 0.089) + (flights * 90)
        energy_total = (electricity * 0.92 * (1 - renewable / 100)) + (natural_gas * 5.3)
        food_base = (red_meat * 6.61) + (poultry * 1.65) + (plant_based * 0.45)
        food_total = food_base - (food_base * (local_food / 100) * 0.15) + (food_waste * 2.5)
        lifestyle_base = (clothing * 20) + (deliveries * 0.5) + (electronics * 300)
        lifestyle_total = lifestyle_base - (lifestyle_base * recycling * 0.3)
        
        total = transport_total + energy_total + food_total + lifestyle_total
        annual = (total * 52) / 1000

        # Save to Database
        Calculation.objects.create(
            user=request.user,
            transport_emissions=transport_total,
            energy_emissions=energy_total,
            food_emissions=food_total,
            lifestyle_emissions=lifestyle_total,
            total_emissions=total,
            annual_emissions=annual
        )

        # Pass results back to the template
        context['results'] = {
            'transport': transport_total, 'energy': energy_total, 'food': food_total,
            'lifestyle': lifestyle_total, 'total': total, 'annual': annual,
        }
    
    return render(request, 'calculator.html', context)

@login_required
def dashboard_view(request):
    calculations = Calculation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'calculations': calculations})