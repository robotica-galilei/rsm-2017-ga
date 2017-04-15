This is the folder used for OCR training and testing

To train the model and generate a generalresponses.data and generalsamples.data you have to import the images for classification in the training_data directory following this structure:

└── training_data
    ├── H
    ├── S
    └── U

The names of the images are not important, nor the order.

After the training using classification.py, testing.py can be used to perform a test using a real-time camera.
