# tap-netsuite

`tap-netsuite` is a Singer tap for Netsuite.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

```bash
pipx install git+https://github.com/sehnem/tap-netsuite
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-netsuite --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

This Singer tap usese TBA authentication for Netsuite, more details can be found [here](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4247337262.html).

## Usage

You can easily run `tap-netsuite` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-netsuite --version
tap-netsuite --help
tap-netsuite --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_netsuite/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-netsuite` CLI interface directly using `poetry run`:

```bash
poetry run tap-netsuite --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-netsuite
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-netsuite --version
# OR run a test `elt` pipeline:
meltano elt tap-netsuite target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.


### Extra config flags

In this tap, we have enabled the possibility of fetching saved searches on Netsuite. To do so, you need to add one or more of the parameters to your config file:

```json
{
    "calendar_event_search_advanced": [your_saved_search_id_here],
    "task_search_advanced": [your_saved_search_id_here],
    "phone_call_search_advanced": [your_saved_search_id_here],
    "file_search_advanced": [your_saved_search_id_here],
    "folder_search_advanced": [your_saved_search_id_here],
    "note_search_advanced": [your_saved_search_id_here],
    "message_search_advanced": [your_saved_search_id_here],
    "item_search_advanced": [your_saved_search_id_here],
    "account_search_advanced": [your_saved_search_id_here],
    "bin_search_advanced": [your_saved_search_id_here],
    "classification_search_advanced": [your_saved_search_id_here],
    "department_search_advanced": [your_saved_search_id_here],
    "location_search_advanced": [your_saved_search_id_here],
    "gift_certificate_search_advanced": [your_saved_search_id_here],
    "sales_tax_item_search_advanced": [your_saved_search_id_here],
    "subsidiary_search_advanced": [your_saved_search_id_here],
    "employee_search_advanced": [your_saved_search_id_here],
    "campaign_search_advanced": [your_saved_search_id_here],
    "promotion_code_search_advanced": [your_saved_search_id_here],
    "contact_search_advanced": [your_saved_search_id_here],
    "customer_search_advanced": [your_saved_search_id_here],
    "partner_search_advanced": [your_saved_search_id_here],
    "vendor_search_advanced": [your_saved_search_id_here],
    "entity_group_search_advanced": [your_saved_search_id_here],
    "job_search_advanced": [your_saved_search_id_here],
    "site_category_search_advanced": [your_saved_search_id_here],
    "support_case_search_advanced": [your_saved_search_id_here],
    "solution_search_advanced": [your_saved_search_id_here],
    "topic_search_advanced": [your_saved_search_id_here],
    "issue_search_advanced": [your_saved_search_id_here],
    "custom_record_search_advanced": [your_saved_search_id_here],
    "time_bill_search_advanced": [your_saved_search_id_here],
    "budget_search_advanced": [your_saved_search_id_here],
    "accounting_transaction_search_advanced": [your_saved_search_id_here],
    "opportunity_search_advanced": [your_saved_search_id_here],
    "transaction_search_advanced": [your_saved_search_id_here],
}
```