# Property Filtering API Guide

This guide explains how to use the new filtering capabilities for properties in the API.

## Overview

The API now supports comprehensive filtering, searching, and ordering for both `HouseForSale` and `HouseForRent` models using django-filter and Django REST Framework's built-in filters.

## Base Endpoints

- **Houses for Sale**: `/api/houses-for-sale/`
- **Houses for Rent**: `/api/houses-for-rent/`

## Filtering Options

### Houses for Sale Filters

#### Price Filters
- `min_price`: Minimum selling price
- `max_price`: Maximum selling price
- `selling_cost`: Exact price
- `selling_cost__gte`: Greater than or equal to price
- `selling_cost__lte`: Less than or equal to price

#### Location Filters
- `city`: City name (case-insensitive partial match)
- `nghood`: Neighborhood (case-insensitive partial match)
- `postal_code`: Exact postal code
- `street`: Street name (exact or partial match)
- `number`: Street number

#### Property Features
- `min_beds` / `max_beds`: Bedroom count range
- `min_baths` / `max_baths`: Bathroom count range
- `beds`: Exact bedroom count
- `baths`: Exact bathroom count

#### Area Filters
- `min_construccion` / `max_construccion`: Construction area range
- `min_superficie` / `max_superficie`: Total surface area range
- `construccion__gte` / `construccion__lte`: Construction area comparison
- `superficie__gte` / `superficie__lte`: Surface area comparison

#### Boolean Filters
- `infonavit`: INFONAVIT eligible (true/false)
- `patio`: Has patio (true/false)
- `negociable`: Price negotiable (true/false)

#### Other Features
- `min_cochera` / `max_cochera`: Garage spaces range
- `min_minisplits` / `max_minisplits`: Air conditioning units range
- `estatus`: Property status (partial match)
- `metodo_de_pago`: Payment method (partial match)
- `servicios`: Available services (partial match)

#### Date Filters
- `created_at__date`: Creation date
- `created_at__date__gte`: Created after date
- `created_at__date__lte`: Created before date
- `updated_at__date`: Update date
- `updated_at__date__gte`: Updated after date
- `updated_at__date__lte`: Updated before date

### Houses for Rent Filters

#### Price Filters
- `min_rent`: Minimum rent cost
- `max_rent`: Maximum rent cost
- `rent_cost`: Exact rent cost
- `rent_cost__gte`: Greater than or equal to rent
- `rent_cost__lte`: Less than or equal to rent

#### Location Filters
- `city`: City name (case-insensitive partial match)
- `nghood`: Neighborhood (case-insensitive partial match)
- `postal_code`: Exact postal code
- `street`: Street name (exact or partial match)
- `number`: Street number

#### Property Features
- `min_bedrooms` / `max_bedrooms`: Bedroom count range
- `min_bathrooms` / `max_bathrooms`: Bathroom count range
- `bedrooms`: Exact bedroom count
- `bathrooms`: Exact bathroom count

#### Boolean Filters
- `garage`: Has garage (true/false)
- `patio`: Has patio (true/false)
- `petfriendly`: Pet friendly (true/false)

#### Other Features
- `min_minisplits` / `max_minisplits`: Air conditioning units range
- `included_services`: Included services (partial match)

## Search Functionality

### Global Search
Use the `search` parameter to search across multiple text fields:

**Houses for Sale:**
- `search`: Searches in title, street, neighborhood, city, comments, status, services, payment method

**Houses for Rent:**
- `search`: Searches in title, street, neighborhood, city, comments, included services

## Ordering

Use the `ordering` parameter to sort results:

### Houses for Sale Ordering Fields
- `selling_cost`: Sort by price
- `beds`: Sort by bedroom count
- `baths`: Sort by bathroom count
- `construccion`: Sort by construction area
- `superficie`: Sort by surface area
- `created_at`: Sort by creation date
- `updated_at`: Sort by update date
- `cochera`: Sort by garage spaces
- `minisplits`: Sort by AC units

### Houses for Rent Ordering Fields
- `rent_cost`: Sort by rent price
- `bedrooms`: Sort by bedroom count
- `bathrooms`: Sort by bathroom count
- `minisplits`: Sort by AC units
- `created_at`: Sort by creation date
- `updated_at`: Sort by update date

**Note:** Use `-` prefix for descending order (e.g., `-selling_cost` for highest price first)

## Pagination

Results are paginated with 20 items per page by default. Use:
- `page`: Page number
- `page_size`: Items per page (if allowed)

## Example API Calls

### Basic Filtering Examples

```bash
# Houses for sale with price range
GET /api/houses-for-sale/?min_price=500000&max_price=1000000

# Houses in specific city with minimum 3 bedrooms
GET /api/houses-for-sale/?city=guadalajara&min_beds=3

# Houses with patio and garage
GET /api/houses-for-sale/?patio=true&min_cochera=1

# Search for houses with "centro" in any text field
GET /api/houses-for-sale/?search=centro

# Sort by price (lowest first)
GET /api/houses-for-sale/?ordering=selling_cost

# Sort by newest first
GET /api/houses-for-sale/?ordering=-created_at

# Combine filters: 3+ bedrooms, 2+ baths, in Guadalajara, under $800k
GET /api/houses-for-sale/?city=guadalajara&min_beds=3&min_baths=2&max_price=800000
```

### Houses for Rent Examples

```bash
# Rent range $5000-$15000
GET /api/houses-for-rent/?min_rent=5000&max_rent=15000

# Pet-friendly houses with garage
GET /api/houses-for-rent/?petfriendly=true&garage=true

# 2+ bedrooms in specific neighborhood
GET /api/houses-for-rent/?nghood=americana&min_bedrooms=2

# Search and sort by rent (lowest first)
GET /api/houses-for-rent/?search=amueblada&ordering=rent_cost
```

### Advanced Filtering Examples

```bash
# Complex filter: Houses for sale
GET /api/houses-for-sale/?city=guadalajara&min_beds=3&max_beds=4&min_price=600000&max_price=900000&patio=true&infonavit=true&ordering=-created_at

# Date range filter
GET /api/houses-for-sale/?created_at__date__gte=2024-01-01&created_at__date__lte=2024-12-31

# Owner-specific properties
GET /api/houses-for-sale/?owner_id=123

# Postal code and area filters
GET /api/houses-for-sale/?postal_code=44100&min_construccion=100&max_superficie=200
```

## Custom Endpoints

### Location-based Search
- `GET /api/houses-for-sale/search_by_location/?city=...&nghood=...&postal_code=...`
- `GET /api/houses-for-rent/search_by_location/?city=...&nghood=...&postal_code=...`

### Price/Rent Range Search
- `GET /api/houses-for-sale/price_range/?min_price=...&max_price=...`
- `GET /api/houses-for-rent/rent_range/?min_rent=...&max_rent=...`

## Response Format

All endpoints return paginated results in this format:

```json
{
    "count": 150,
    "next": "http://localhost:8000/api/houses-for-sale/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Casa en venta",
            "selling_cost": 750000,
            "beds": 3,
            "baths": 2.5,
            "city": "Guadalajara",
            "nghood": "Americana",
            "images": [...],
            // ... other fields
        }
    ]
}
```

## Frontend Integration Tips

1. **Build Dynamic Filters**: Create form controls for each filter parameter
2. **Combine Filters**: Multiple filters can be used together in a single request
3. **Implement Search**: Add a search box that uses the `search` parameter
4. **Add Sorting**: Provide dropdown or buttons for different ordering options
5. **Handle Pagination**: Implement pagination controls using the `next`/`previous` URLs
6. **URL State**: Consider updating the browser URL to reflect current filters for bookmarking

## Error Handling

- Invalid filter values return 400 Bad Request
- Non-existent fields are ignored
- Date filters expect YYYY-MM-DD format
- Boolean filters accept: true, false, 1, 0

This filtering system provides powerful and flexible property search capabilities for your frontend application.