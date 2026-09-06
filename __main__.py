
from cars.sedan import Sedan
from cars.off_road import off_road
from cars.sport_car import sport_car

def main():

    cars = [
        Sedan('Toyota', 'Camry', 2020, 4, 'independent', 5),
        Sedan('Honda', 'Accord', 2021, 4, 'independent', 5),
        Sedan('Ford', 'Fusion', 2019, 4, 'independent', 5),
        Sedan('Chevrolet', 'Malibu', 2020, 4, 'independent', 5),
        Sedan('Nissan', 'Altima', 2021, 4, 'independent', 5),
        Sedan('Hyundai', 'Sonata', 2020, 4, 'independent', 5),
        Sedan('Kia', 'Optima', 2021, 4, 'independent', 5),
        Sedan('Mazda', '6', 2019, 4, 'independent', 5),
        Sedan('Volkswagen', 'Passat', 2020, 4, 'independent', 5),
        Sedan('Subaru', 'Legacy', 2021, 4, 'independent', 5),
        Sedan('Toyota', 'Camry', 2020, 4, 'independent', 5),

        off_road('Jeep', 'Wrangler', 2020, 250, 'manual', True),
        off_road('Land Rover', 'Defender', 2021, 300, 'automatic', True),
        off_road('Toyota', 'Land Cruiser', 2019, 280, 'automatic', True),
        off_road('Ford', 'Bronco', 2020, 270, 'manual', True),
        off_road('Chevrolet', 'Blazer', 2021, 260, 'automatic', True),
        off_road('Nissan', 'Xterra', 2020, 250, 'manual', True),
        off_road('Jeep', 'Cherokee', 2021, 240, 'automatic', True),
        off_road('Toyota', '4Runner', 2020, 230, 'manual', True),
        off_road('Land Rover', 'Discovery', 2021, 220, 'automatic', True),
        off_road('Ford', 'Ranger', 2020, 210, 'manual', True),

        sport_car('Porsche', '911', 2020, 330, 3.5, 'disc'),
        sport_car('Ferrari', '488', 2021, 330, 3.0, 'disc'),
        sport_car('Lamborghini', 'Huracan', 2019, 325, 3.2, 'disc'),
        sport_car('McLaren', '720S', 2020, 341, 2.9, 'disc'),
        sport_car('Aston Martin', 'Vantage', 2021, 314, 3.6, 'disc'),
        sport_car('Chevrolet', 'Corvette', 2020, 312, 3.7, 'disc'),
        sport_car('Nissan', 'GT-R', 2021, 315, 3.8, 'disc'),
        sport_car('BMW', 'M4', 2020, 290, 4.0, 'disc'),
        sport_car('Audi', 'R8', 2021, 330, 3.9, 'disc'),    
        sport_car('Mercedes-Benz', 'AMG GT', 2020, 310, 4.1, 'disc')
    ]

    print (f"Total number of cars: {len(cars)}\n")
    print("=" * 50)

    for i, car in enumerate(cars):
        car_type = car.__class__.__name__.upper()
        brand = car.get_parameters('brand')
        model = car.get_parameters('model') 
        year = car.get_parameters('year')

        print(f"[{i}] Type: {car_type} | Car: {brand} {model} ({year})")
        print("Parameters:")

        for key, value in car.parameters.items():
            print(f"  - {key}: {value}")

        print("-" * 50)

if __name__ == "__main__":
    main()
