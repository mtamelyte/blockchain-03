// merkle.cpp
#include <bitcoin/bitcoin.hpp>

// Merkle Root Hash
bc::hash_digest create_merkle(bc::hash_list &merkle)
{
    // Stop if hash list is empty or contains one element
    if (merkle.empty())
        return bc::null_hash;
    else if (merkle.size() == 1)
        return merkle[0];
    // While there is more than 1 hash in the list, keep looping...
    while (merkle.size() > 1)
    {
        // If number of hashes is odd, duplicate last hash in the list.
        if (merkle.size() % 2 != 0)
            merkle.push_back(merkle.back());
        // List size is now even.
        assert(merkle.size() % 2 == 0);
        // New hash list.
        bc::hash_list new_merkle;
        // Loop through hashes 2 at a time.
        for (auto it = merkle.begin(); it != merkle.end(); it += 2)
        {
            // Join both current hashes together (concatenate).
            bc::data_chunk concat_data(bc::hash_size * 2);
            auto concat = bc::serializer<
                decltype(concat_data.begin())>(concat_data.begin());
            concat.write_hash(*it);
            concat.write_hash(*(it + 1));
            // Hash both of the hashes.
            bc::hash_digest new_root = bc::bitcoin_hash(concat_data);
            // Add this to the new list.
            new_merkle.push_back(new_root);
        }
        // This is the new list.
        merkle = new_merkle;
        // DEBUG output -------------------------------------
        std::cout << "Current merkle hash list:" << std::endl;
        for (const auto &hash : merkle)
            std::cout << " " << bc::encode_hash(hash) << std::endl;
        std::cout << std::endl;
        // --------------------------------------------------
    }
    // Finally we end up with a single item.
    return merkle[0];
}

int main()
{
    // Transactions hashes from a block (#100 000) to reproduce the same merkle root
    bc::hash_list tx_hashes{{
        bc::hash_literal("bcdc61cbecf6137eec5c8ad4047fcdc36710e77e404b17378a33ae605920afe1"),
        bc::hash_literal("f7f4c281ee20ab8d1b00734b92b60582b922211a7e470accd147c6d70c9714a3"),
        bc::hash_literal("b5f6e3b217fa7f6d58081b5d2a9a6607eebd889ed2c470191b2a45e0dcb98eb0"),
        bc::hash_literal("4206f171f06913b1d40597edcaf75780559231fb504c49ba85a4a9ae949e8b95"),
        bc::hash_literal("a1a6ad6ff321c76496a89b6a4eb9bcfb76b9e068b677d5c7d427c51ca08c273d"),
        bc::hash_literal("89c82039452c14a9314b5834e5d2b9241b1fdccdb6e4f4f68e49015540faaf95"),
        bc::hash_literal("25c6a1f8c0b5be2bee1e8dd3478b4ec8f54bbc3742eaf90bfb5afd46cf217ad9"),
        bc::hash_literal("57eef4da5edacc1247e71d3a93ed2ccaae69c302612e414f98abf8db0b671eae"),
        bc::hash_literal("8d30eb0f3e65b8d8a9f26f6f73fc5aafa5c0372f9bb38aa38dd4c9dd1933e090"),
        bc::hash_literal("13e3167d46334600b59a5aa286dd02147ac33e64bfc2e188e1f0c0a442182584"),
    }};
    const bc::hash_digest merkle_root = create_merkle(tx_hashes);
    std::cout << "Merkle Root Hash: " << bc::encode_hash(merkle_root) << std::endl;
    // std::cout << "Merkle Root Hash-2: " << bc::encode_hash(merkle_root) << std::endl;
    return 0;
}