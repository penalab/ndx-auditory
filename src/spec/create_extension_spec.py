# -*- coding: utf-8 -*-
import pathlib

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec
from pynwb.spec import NWBDatasetSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="ndx-auditory",
        version="0.1.0",
        doc="""Auditory stimuli""",
        author=[
            "Roland Ferger",
        ],
        contact=[
            "roland.ferger@einsteinmed.edu",
        ],
    )
    ns_builder.include_namespace("core")

    # TODO: if your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-other-extension")

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    # tetrode_series = NWBGroupSpec(
    #     neurodata_type_def="TetrodeSeries",
    #     neurodata_type_inc="ElectricalSeries",
    #     doc="An extension of ElectricalSeries to include the tetrode ID for each time series.",
    #     attributes=[NWBAttributeSpec(name="trode_id", doc="The tetrode ID.", dtype="int32")],
    # )
    auditory_device = NWBGroupSpec(
        neurodata_type_def="AuditoryDevice",
        neurodata_type_inc="Device",
        doc="Metadata about an device used to present auditory stimuli",
    )

    auditory_tracks_table = NWBGroupSpec(
        name="auditory_tracks",
        neurodata_type_inc="DynamicTable",
        doc="A table of all tracks for auditory stimuli available for this experiments.",
        quantity="?",
        datasets=[
            NWBDatasetSpec(
                name="device",
                dtype=NWBRefSpec(target_type="AuditoryDevice", reftype="object"),
                doc="Reference to the AuditoryDevice this track was connected to.",
            ),
            NWBDatasetSpec(
                name="presentation",
                dtype="text",
                doc="Presentation type like 'free field', 'dichotic', 'virtual'.",
            ),
        ],
    )

    auditory_stimuli_meta = NWBGroupSpec(
        name="auditory_stimulation",
        doc="Metadata related to auditory stimuli.",
        quantity="?",
        groups=[auditory_tracks_table],
    )

    auditory_stimuli_series = NWBGroupSpec(
        neurodata_type_def="AuditoryStimulusSeries",
        neurodata_type_inc="TimeSeries",
        doc="A TimeSeries for Auditory Stimuli",
        attributes=[],
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="waveforms of auditory stimuli",
                dtype="numeric",
                shape=((None, 1), (None, None)),
                dims=(("time", "track"), ("time", "tracks")),
                attributes=[
                    NWBAttributeSpec(
                        name="unit",
                        doc="SI unit of data",
                        dtype="text",
                        value="n.a.",
                    )
                ],
            ),
            NWBDatasetSpec(
                name="tracks",
                neurodata_type_inc="DynamicTableRegion",
                doc="DynamicTableRegion pointer to the auditory_tracks that are saved in this time series.",
            ),
            NWBDatasetSpec(
                name="stimuli",
                neurodata_type_inc="DynamicTable",
                doc="DynamicTable identifying all stimuli that are saved in this time series.",
            ),
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [auditory_stimuli_meta, auditory_device, auditory_stimuli_series]

    # export the spec to yaml files in the spec folder
    output_dir = str((pathlib.Path(__file__).parent.parent.parent / "spec").resolve())
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
