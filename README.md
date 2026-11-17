# SynapSoul Relay Guide

[SynapSoul Relay](https://relay.synapsoullabs.tech/) prepares approved web and media inputs for downstream use. It can turn HTML into clean text, import WebVTT transcripts, and publish segmented audio bundles. Exports include source citations, usage metadata, and content hashes so you can trace what went into a dataset.

## Try it in two minutes

The public site explains Relay and shows its verified local benchmark. This guide includes a downloadable sample you can use today. It uses invented sources and runs offline with Python 3.12 or later.

1. Download this repository using GitHub's **Code → Download ZIP** and extract it.
2. Open a terminal in the extracted folder.
3. Verify the sample export and print its source citations.

   ```sh
   python examples/inspect_export.py examples/sample-manifest.json examples/sample.jsonl
   ```

You should see **Verified version 1 with 2 records** followed by a source citation for each record. Open [sample.jsonl](examples/sample.jsonl) to see the text payload and provenance side by side. Try changing a word in a copy of the export and running the same command against that copy. The checksum should fail.

## Use an export in your workflow

| Goal | Start with | Check before importing |
| --- | --- | --- |
| Make documents searchable | Clean HTML text or WebVTT transcripts in JSONL | Confirm the source permits search indexing. Keep the original URL and source revision alongside each result. |
| Build a research collection | A pinned JSONL export with source proofs | Carry citations into your index. Confirm that the intended AI use is allowed if an assistant will read the collection. |
| Prepare a training corpus | A text export approved for the intended training purpose | Check training and commercial permissions for the actual use. Keep source provenance with the corpus. |
| Analyze a larger dataset | Parquet when available | Pin the version and retain the manifest, file checksum, and source proofs. |

## Work with your own sources

The public website is a product and benchmark page. Live job submission requires access to a Relay deployment and a tenant credential from its operator.

1. Give your operator the source URLs or IDs, evidence that the proposed use is allowed, and the output you need. Ask for an existing transcript first if your workflow only needs text.
2. Review the pre-flight byte and cost estimate. Agree on budget caps before submitting the job.
3. Track the job until it publishes a dataset. If a budget cap pauses the job, review the estimate and settled usage with your operator before resuming.
4. Download the manifest and the file for the same dataset version. Use the manifest to verify the file's size and SHA-256, and keep it with your imported copy.
5. Use the export only for the authorized purpose. Verify current permissions with your operator when reusing an older export or changing how you use it.

### Read the manifest and records

- **Dataset version and record count** identify the snapshot and the number of records to expect.
- **File size and SHA-256** verify the downloaded bytes. JSONL and Parquet have separate file hashes.
- **Record ID and content hash** let you track records and compare content across exports.
- **Provenance** ties each record to a source URL, source revision, fetch time, and usage metadata.

The sample checker verifies the JSONL file against the supplied manifest and displays its citations. Your operator remains the authority for current permissions and for authenticating a manifest from a live deployment.
