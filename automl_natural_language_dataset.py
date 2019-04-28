#!/usr/bin/env python

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on Dataset
with the Google AutoML Natural Language API.
For more information, see the tutorial page at
https://cloud.google.com/natural-language/automl/docs/
"""

import argparse
import os


def create_dataset(project_id, compute_region, dataset_name):
    """Create a dataset."""
    # [START automl_language_create_dataset]
    # TODO(developer): Uncomment and set the following variables
    multilabel = True;
     

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # Classification type is assigned based on multilabel value.
    classification_type = "MULTICLASS"
    if multilabel:
        classification_type = "MULTILABEL"

    # Specify the text classification type for the dataset.
    dataset_metadata = {"classification_type": classification_type}

    # Set dataset name and metadata.
    my_dataset = {
        "display_name": dataset_name,
        "text_classification_dataset_metadata": dataset_metadata,
    }

    # Create a dataset with the dataset metadata in the region.
    dataset = client.create_dataset(project_location, my_dataset)

    # Display the dataset information.
    print("Dataset name: {}".format(dataset.name))
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print("Dataset display name: {}".format(dataset.display_name))
    print("Text classification dataset metadata:")
    print("\t{}".format(dataset.text_classification_dataset_metadata))
    print("Dataset example count: {}".format(dataset.example_count))
    print("Dataset create time:")
    print("\tseconds: {}".format(dataset.create_time.seconds))
    print("\tnanos: {}".format(dataset.create_time.nanos))

    # [END automl_language_create_dataset]


def list_datasets(project_id, compute_region, filter_):
    """List all datasets."""
    # [START automl_language_list_datasets]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # filter_ = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # List all the datasets available in the region by applying filter.
    response = client.list_datasets(project_location, filter_)

    print("List of datasets:")
    for dataset in response:
        # Display the dataset information.
        print("Dataset name: {}".format(dataset.name))
        print("Dataset id: {}".format(dataset.name.split("/")[-1]))
        print("Dataset display name: {}".format(dataset.display_name))
        print("Text classification dataset metadata:")
        print("\t{}".format(dataset.text_classification_dataset_metadata))
        print("Dataset example count: {}".format(dataset.example_count))
        print("Dataset create time:")
        print("\tseconds: {}".format(dataset.create_time.seconds))
        print("\tnanos: {}".format(dataset.create_time.nanos))

    # [END automl_language_list_datasets]


def get_dataset(project_id, compute_region, dataset_id):
    """Get the dataset."""
    # [START automl_language_get_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Get complete detail of the dataset.
    dataset = client.get_dataset(dataset_full_id)

    # Display the dataset information.
    print("Dataset name: {}".format(dataset.name))
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print("Dataset display name: {}".format(dataset.display_name))
    print("Text classification dataset metadata:")
    print("\t{}".format(dataset.text_classification_dataset_metadata))
    print("Dataset example count: {}".format(dataset.example_count))
    print("Dataset create time:")
    print("\tseconds: {}".format(dataset.create_time.seconds))
    print("\tnanos: {}".format(dataset.create_time.nanos))

    # [END automl_language_get_dataset]


def import_data(project_id, compute_region, dataset_id, path):
    """Import labelled items."""
    # [START automl_language_import_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # path = 'gs://path/to/file.csv'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Get the multiple Google Cloud Storage URIs.
    input_uris = path.split(",")
    input_config = {"gcs_source": {"input_uris": input_uris}}

    # Import the dataset from the input URI.
    response = client.import_data(dataset_full_id, input_config)

    print("Processing import...")
    # synchronous check of operation status.
    print("Data imported. {}".format(response.result()))

    # [END automl_language_import_data]


def export_data(project_id, compute_region, dataset_id, output_uri):
    """Export a dataset to a Google Cloud Storage bucket."""
    # [START automl_language_export_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # output_uri: 'gs://location/to/export/data'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Set the output URI
    output_config = {"gcs_destination": {"output_uri_prefix": output_uri}}

    # Export the data to the output URI.
    response = client.export_data(dataset_full_id, output_config)

    print("Processing export...")
    # synchronous check of operation status.
    print("Data exported. {}".format(response.result()))

    # [END automl_language_export_data]


def delete_dataset(project_id, compute_region, dataset_id):
    """Delete a dataset."""
    # [START automl_language_delete_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Delete a dataset.
    response = client.delete_dataset(dataset_full_id)

    # synchronous check of operation status.
    print("Dataset deleted. {}".format(response.result()))

    # [END automl_language_delete_dataset]


if __name__ == "__main__":
    
    create_dataset('cdmx-safe-map','us-east4','Crimecategory')
    print("dataset created")
    
    import_data('cdmx-safe-map','us-east4','Crimecategory','Delitos.csv')
    
   
