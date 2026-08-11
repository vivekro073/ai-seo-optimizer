import os
from urllib.parse import urljoin
from crawlee.storage_clients import SqlStorageClient
from crawlee.crawlers import ParselCrawler, ParselCrawlingContext
from dotenv import load_dotenv

load_dotenv()

async def scraper(website):
    db_url = os.environ.get('DATABASE_URL')

    if db_url and db_url.startswith("postgresql://"):
        # 1. Swap the protocol to asyncpg
        async_db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        async_db_url = async_db_url.split("?")[0]
    else:
        async_db_url = db_url

    async with SqlStorageClient(connection_string=async_db_url) as storage_client:
        # 1. Initialize the SINGLE crawler instance with your storage client
        crawler = ParselCrawler(storage_client=storage_client)

        # 2. Attach the handler directly to THIS instance's router
        @crawler.router.default_handler
        async def request_handler(context: ParselCrawlingContext) -> None:
            current_url = context.request.url
            page_status = context.http_response.status_code

            context.log.info(f'Processing {current_url} ...')

            # Extract all raw links from the page
            links = context.selector.css('a')

            page_links_data = []
            # Loop through the array and push each link as its own dictionary
            for link in links:
                href = link.css('::attr(href)').get()
                if href:
                    anchor_text = link.xpath('normalize-space(.)').get()

                    # 2. Append to the list instead of calling the database
                    page_links_data.append({
                        'source_page': current_url,
                        'target_link': urljoin(current_url, href),
                        'anchor_text': anchor_text if anchor_text else "No Text",
                        'source_status': page_status
                    })

                # 3. Push the entire list in ONE single network call
            if page_links_data:
                await context.push_data(page_links_data)

            await context.enqueue_links()

            # 3. Run the crawler
        await crawler.run([website])


# if __name__ == '__main__':
#     asyncio.run(main())
