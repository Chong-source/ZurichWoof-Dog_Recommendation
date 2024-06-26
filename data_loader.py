"""
© Copyright 2024 Kai Lo and Chong Wan
Loads data from all 7 of our different datasets for this project.

Each source pertains to a different part of the recommendation process.

Some datasets were found online, and some of them were generated by us (mainly using Google
Translate/Maps/Geocode/Search APIs) and then manually cleaned and inspected.
"""
import csv
import math
from dataclasses import dataclass

from districts import District
from graphs import Graph, WeightedGraph
from userdata import User


@dataclass
class UserPreferenceDogBreed:
    """A class of dog breed that stores information about each breed that stores the dog's rating
    of each trait based off of the data collected by the american Kennel Club:
    https://www.kaggle.com/datasets/sujaykapadnis/dog-breeds"""
    breed_name: str
    affectionate_w_family: int  # positive trait
    good_w_young_children: int  # positive trait
    good_w_other_dog: int  # positive trait
    shedding_level: int  # do negative weight -> negative trait
    openness_to_strangers: int  # positive trait
    playfulness: int  # positive
    protective_nature: int  # positive
    adaptability: int  # positive
    trainability: int  # positive
    energy: int  # Let users decide
    barking: int  # negative trait
    stimulation_needs: int  # Let users decide


def load_dog_data(dog_data_file: str, districts: set[District]) -> tuple[Graph, WeightedGraph]:
    """Creates two graphs:
        - a graph containing every user in the given dog data file,
            and every dog breed with edges between owners and pets.
        - a weighted graph containing every district in the given dog data file,
            and every dog breed with weighted edges between districts and # of dogs from breed

    Ignores Mischling/mixed-breed dogs.
    """
    dog_graph = Graph()
    district_graph = WeightedGraph()
    district_mapping = {target.district_id: target for target in districts}
    users = {}
    with open(dog_data_file, encoding='utf-8') as dog_data_content:
        reader = csv.reader(dog_data_content)
        next(reader, None)  # Skip the first line header
        for row in reader:
            user_id = int(row[0])
            raw_age_range = row[1]
            if not raw_age_range.strip():
                continue  # Missing age range
            gender = row[2].upper()
            if not gender.strip():
                continue  # Missing gender data
            district_id = int(row[4])
            if district_id not in district_mapping:
                continue  # Invalid district ID
            district = district_mapping[district_id]
            dog_breed = row[5].capitalize()
            if 'Mischling' in dog_breed:  # Ignore mix-breed dogs because its complicated
                continue
            split_age_range = raw_age_range.split('-')
            age = (int(split_age_range[0]) + int(split_age_range[1])) // 2  # Average in age range
            if user_id not in district_mapping:
                users[user_id] = User(user_id, age, gender, district)
                dog_graph.add_vertex(users[user_id])
            user = users[user_id]
            dog_graph.add_vertex(dog_breed)
            dog_graph.add_edge(dog_breed, user)

            if not district_graph.contains(user.district):
                district_graph.add_vertex(user.district)
            if not district_graph.contains(dog_breed):
                district_graph.add_vertex(dog_breed)
            current_weight = district_graph.get_weight(user.district, dog_breed)
            district_graph.add_edge(user.district, dog_breed, current_weight + 1)
    return dog_graph, district_graph


def load_district_data(district_data_file: str) -> set[District]:
    """Loads the set of districts from a given district data file,
    that contains each district's name and ID number.
    """
    with open(district_data_file, encoding='utf-8') as districts_data:
        reader = csv.reader(districts_data)
        districts = set()
        next(reader, None)
        for row in reader:
            # Sample row: ['261031', '31', 'Alt-Wiedikon', '261', '169']
            district = District(int(row[1]), row[2])
            districts.add(district)
        return districts


def get_raw_district_distances(
        districts: set[District],
        district_distance_file: str
) -> dict[District, dict[District, float]]:
    """Takes existing district data and creates a mapping between districts and their distance
    to every other district by loading data from the CSV file at district_distance_file.

    Raw data in this context means it has not been normalized (and remains in kilometers,
    not bounded by 0.0 and 1.0)
    """
    district_lookup = {target.district_id: target for target in districts}
    raw_district_distances = {}
    with open(district_distance_file) as district_distance_content:
        reader = csv.reader(district_distance_content)
        next(reader, None)
        for row in reader:
            district_id = row[0]
            origin = district_lookup[int(district_id)]
            if not origin:
                continue
            district_distances = {}
            district_mapping_raw = row[1].split('|')
            for mapping in district_mapping_raw:
                mapping_split = mapping.split(':')
                destination_id, distance = int(mapping_split[0]), float(mapping_split[1])
                destination = district_lookup[destination_id]
                if not destination or destination == origin:
                    continue
                district_distances[destination] = distance
            raw_district_distances[origin] = district_distances
    return raw_district_distances


def normalize_district_distances(raw_district_distances: dict[District, dict[District, float]]) -> None:
    """Normalize district distances so that all of them are between 0.0 and 1.0 (from raw km data).
    In this case, also flips the values so that 1.0 indicates close districts and 0.0 is far.
    Mutates the given dictionary.
    """
    min_distance = math.inf
    max_distance = 0
    for origin in raw_district_distances:
        for destination in raw_district_distances[origin]:
            assert origin != destination
            distance = raw_district_distances[origin][destination]
            min_distance = min(distance, min_distance)
            max_distance = max(distance, max_distance)
    if max_distance == 0:
        raise ValueError
    difference = max_distance - min_distance
    for origin in raw_district_distances:
        for destination in raw_district_distances[origin]:
            distance = raw_district_distances[origin][destination]
            distance -= min_distance
            distance /= difference
            distance = 1 - distance
            raw_district_distances[origin][destination] = distance
            assert 0.0 <= distance <= 1.0


def apply_district_distances(district_distances: dict[District, dict[District, float]]) -> None:
    """Mutates the distance attributes of each district in the district_distances dictionary
    so that it has the distance values corresponding to our given dictionary.
    """
    for origin in district_distances:
        for destination in district_distances[origin]:
            assert origin != destination
            origin.set_distance(destination, district_distances[origin][destination])


def dog_breed_data_loader(file: str) -> list[UserPreferenceDogBreed]:
    """Loads the data from the breed_traits.csv file, creates a list of DogBreed objects"""
    with open(file) as dog_breed_file:
        dog_breed_file.readline()
        breed_informations = []
        dog_breed_rows = csv.reader(dog_breed_file)
        for row in dog_breed_rows:
            breed_informations.append(
                UserPreferenceDogBreed(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]),
                                       int(row[6]), int(row[7]), int(row[8]), int(row[9]), int(row[10]),
                                       int(row[11]), int(row[12])))
        return breed_informations


def load_district_lat_lng(file: str, districts: set[District]) -> dict[District, tuple[float, float]]:
    """Loads the district latitudes and longitudes from a mapping file.
    """
    district_lookup = {target.district_name: target for target in districts}
    with open(file, encoding='utf-8') as district_file:
        district_file.readline()
        district_rows = csv.reader(district_file)
        district_dict = {}
        for row in district_rows:
            district_name, lat, lng = row[0], float(row[1]), float(row[2])
            district = district_lookup[district_name]
            district_dict[district] = (lat, lng)
        return district_dict


def load_translation_mapping(file: str) -> dict[str, str]:
    """Loads the mapping between german dog names to english dog names from a file.
    """
    with open(file, encoding='utf-8') as translation_file:
        translation_file.readline()
        translation_rows = csv.reader(translation_file)
        translation_dict = {}
        for row in translation_rows:
            translation_dict[row[0]] = row[1]  # German to english
        return translation_dict


def load_dog_images(file: str) -> dict[str, str]:
    """Loads the mapping between ENGLISH dog names and images URLs online.
    """
    with open(file) as images_file:
        images_file.readline()
        images_rows = csv.reader(images_file)
        images_dict = {}
        for row in images_rows:
            images_dict[row[0]] = row[1]
        return images_dict
