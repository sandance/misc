#!/bin/bash

sed -i '1 i --skip_jobs\nPenetration,GenerateArrivalDeparturesMatrix,GenerateTripLegMatrix,GenerateHomeWorkMatrix' dagjobsfull.cfg
