from ..models.magazine import Magazine

def seed():
    magazines = [
        ("Tech Weekly", "Technology"),
        ("Health Digest", "Health"),
        ("Fashion Forward", "Fashion"),
        ("Finance Daily", "Finance"),
        ("Science Now", "Science"),
        ("Sports Monthly", "Sports"),
        ("Art & Culture", "Culture"),
    ]

    for name, category in magazines:
        existing = Magazine.find_by_name(name)
        if not existing:
            mag = Magazine(name=name, category=category)
            mag.save()
            print(f"Seeded magazine: {name} ({category})")
        else:
            print(f"Magazine already exists: {name}")
