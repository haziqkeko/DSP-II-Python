import pandas as pd

# [HAZIQ] CONSTANTS FOR FEES
DELIVERY_FLAT_RATE = 85.00
INSTALLATION_FLAT_RATE = 450.00

# [KER QIN] MATERIAL DATAFRAME
def load_data():
    data = {
        "Material": [
            "Vinyl", "Marble", "Solid Wood", "Ceramic Tile", "Porcelain Tile",
            "Standard Paint", "Premium Wallpaper", "Textured Paint"
        ],
        "Type": [
            "Floor", "Floor", "Floor", "Floor", "Floor",
            "Wall", "Wall", "Wall"
        ],
        "Price_Per_Sqm": [
            55.00, 165.00, 270.00, 85.00, 110.00,
            22.00, 65.00, 95.00
        ],
        "Is_Waterproof": [
            True, True, False, True, True,
            False, False, True
        ],
        "Image_File": [
            "images/vinyl.jpg",
            "images/marble.jpg",
            "images/wood.jpg",
            "images/ceramic.jpg",
            "images/porcelain.jpg",
            "images/paint.jpg",
            "images/wallpaper.jpg",
            "images/texture.jpg"
        ]
    }
    return pd.DataFrame(data)
df = load_data()

# [HAZIQ]
class RenovationLogic:
    @staticmethod
    def check_safety(room_type, floor_mat):
        try:
            material_data = df[df['Material'] == floor_mat].iloc[0]
        except IndexError:
            return False, "Error: Material not found."

        if room_type in ["Bathroom", "Kitchen"] and not material_data['Is_Waterproof']:
            return False, (
                f"SAFETY WARNING: '{floor_mat}' is not suitable for wet areas like {room_type}s.\n"
                "It is highly susceptible to rotting, warping, or mold."
            )
        return True, ""

    @staticmethod
    def calculate_project(width, length, height, floor_mat, wall_mat, tile_size_str):
        # ROOM CALCULATIONS
        area_sqm = width * length
        perimeter = 2 * (width + length)
        wall_area = perimeter * height

        # RETRIEVE PRICES
        f_row = df[df['Material'] == floor_mat].iloc[0]
        w_row = df[df['Material'] == wall_mat].iloc[0]

        f_price = f_row['Price_Per_Sqm']
        w_price = w_row['Price_Per_Sqm']

        # [AIMAN] WASTAGE LOGIC FOR TILE SIZE
        tile_wastage = {
            "30x30 cm": 1.05,
            "60x60 cm": 1.08,
            "15x90 cm": 1.12
        }
        wastage_factor = tile_wastage.get(tile_size_str, 1.05)

        # [HAZIQ] TILE CALCULATION
        try:
            dims = tile_size_str.lower().replace(' cm', '').split('x')
            one_tile_area_sqm = (int(dims[0]) / 100) * (int(dims[1]) / 100)
        except:
            one_tile_area_sqm = 0.09

        # [AIMAN] ADD WASTAGE FACTOR TO CALCULATION
        tiles_needed = int((area_sqm / one_tile_area_sqm) * wastage_factor)
        floor_cost = area_sqm * f_price * wastage_factor
        wall_cost = wall_area * w_price
        total_cost = floor_cost + wall_cost

        return {
            "tiles_needed": tiles_needed,
            "wall_area": wall_area,
            "floor_area": area_sqm,
            "floor_price": f_price,
            "wall_price": w_price,
            "total_cost": total_cost,
            "floor_cost": floor_cost,
            "wall_cost": wall_cost,
            "floor_img": f_row['Image_File'],
            "wall_img": w_row['Image_File']
        }