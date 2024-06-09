## Automation of adding new products to the store.

1. Update feed files from the drop-shipping portals.
2. Extract product files into one format.
3. Filter products by name, category, or sku - to insrt products you need to choose them somehow.
   That could be done manually on the website, or you can select bunch of products based on their name, category or sku.
   This filtered products will be a base for the next steps.
4. Add a single product by SKU.
5. Add multiple products from a CSV file.
6. Both options need to be available for the vidaXL and BigBuy drop-shipping portals.
7. Translate the product description into the english language.
8. Translate the product description into the Polish language.
9. Translate the product description into the Dutch language.
10. Generate missing product information (e.g., product clickable name, product description, category)
    Generate seo information (e.g., meta title, meta description, meta keywords).

## Implementation

1. The feed files updator are implemented.

   The VidaXL file feed is updated by downloading the file from the url. It is one file around 600 MB.
   Vida says that the file is updated every 1-2 hours with the stock and price information.

   The BigBuy file feed updator is downloading all files in the provided languages. The files for 3 languages are almost
   4GB.
   The languages can be set in the settings file.
   Both feeds has the feed update interval set in the settings file. Number is in hours and is used to determine if the
   feed needs to be updated.

   Once the feed is updated, there is a feed extractor which is extracting the products from the feed files.
   What does extract means:

    - it's saving files in the csv format with ';' as delimiter,
    - it is changing the general column names to the same ones in all files - the names for columns are set in the
      settings
      file,
    - it is merging all big buy files into one file to have all products in one file,

2. Add a single product by SKU.

   There is Product Management Service which has a managers attached to it:
    - Presta Product Manager - responsible for adding products to the PrestaShop store,
    - Presta Category Manager - responsible for adding categories to the PrestaShop store in case they are missing,
    - Presta Brand Manager - responsible for adding brands to the PrestaShop store in case they are missing,
    - GPT SEO Manager - responsible for generating seo information for the products, categories and brands,
    - GPT Product Manager - responsible for generating missing product information for the products,
    - GPT Category Manager - responsible for generating missing category information for the products,
    - GPT Brand Manager - responsible for generating missing brand information for the products,

   Service has a method to verify the product information and add it to the store.
   During verification GPT managers are called to generate missing information and Presta managers are called to add
   missed information to the store.
   After all information is added, the product is added to the store.

   Features to implement for product management service are translation of all the product information.

