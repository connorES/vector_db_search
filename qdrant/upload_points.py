def upload_points(client, collection, points, chunk_size=1000):
    # Upload the points in chunks
    for i in range(0, len(points), chunk_size):
        chunk = points[i:i+chunk_size]
        client.upsert(
            collection_name=collection,
            points=chunk
        )
        print(f"Uploaded {len(chunk)} points (chunk {i//chunk_size + 1})")

    print(f"Total points uploaded: {len(points)}")
