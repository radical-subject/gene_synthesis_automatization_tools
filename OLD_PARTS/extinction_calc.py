import sys

from Bio.Alphabet import IUPAC
from Bio.Seq import Seq

seq01 = Seq("acgt", IUPAC.unambiguous_dna)
# arguments for script (input file name, PCR volume, required number of PCR reactions, SPE elution
# volume)
scheme_file_name = sys.argv[1]
reaction_volume = float(sys.argv[2])
number_of_reactions = float(sys.argv[3])
elution_volume = float(sys.argv[4])


# calculation of oligo extinction coefficients
def e260_func(seq):
    Coefficients = {
        "a": 15.4,
        "c": 7.4,
        "g": 11.5,
        "t": 8.7,
        "aa": 13.7,
        "ac": 10.6,
        "ag": 12.5,
        "at": 11.4,
        "ca": 10.6,
        "cc": 7.3,
        "cg": 9,
        "ct": 7.6,
        "ga": 12.6,
        "gc": 8.8,
        "gg": 10.8,
        "gt": 10,
        "ta": 11.7,
        "tc": 8.1,
        "tg": 9.5,
        "tt": 8.4,
    }
    e260 = 0
    for i in range(0, len(seq) - 1):
        e260 = e260 + 2 * Coefficients[seq[i] + seq[i + 1]]
    for i in range(0, len(seq) - 2):
        e260 = e260 - Coefficients[seq[i + 1]]
    return e260


# Input format for TBIO calculation:
# Name Sequence Yield, % Target Concentration, nMA260 (1 cm)
oligos_table = [
    [
        "Name",
        "Sequence",
        "Yield, %",
        "e260, mM-1cm-1",
        "A260, (1cm)",
        "Concentration, nM",
        "Target Concentration, nM",
        "V, ul",
        "Vnorm, ul",
    ]
]
volumes = []
total_volume_for_reaction = 0
total_volume_for_mixing = 0
A260_afterSPE_exp = 0
# reading input file
with open(scheme_file_name) as scheme_file:
    lines = scheme_file.readlines()
lines = lines[1 : len(lines)]
for line in lines:
    Name = line.split("\t")[0]
    Sequence = line.split("\t")[1]
    Yield = float(line.split("\t")[2])
    e260 = e260_func(line.split("\t")[1].lower())
    A260 = float(line.split("\t")[4])
    Concentration = (
        A260 / (e260 + (e260 / 2) * (1 - (Yield / 100)) / (Yield / 100)) * 1000000
    )
    Target_Concentration = float(line.split("\t")[3])
    V = reaction_volume / (Concentration / Target_Concentration)
    Vnorm = reaction_volume / (Concentration / Target_Concentration)
    oligos_table.append(
        [
            Name,  # 0
            Sequence,
            Yield,
            str(round(e260, 5)),
            str(A260),
            str(round(Concentration, 5)),
            str(Target_Concentration),
            str(round(V, 5)),
            str(round(Vnorm, 5)),
        ]
    )
for oligo in oligos_table:
    if oligo[7] != "V, ul":
        total_volume_for_reaction = total_volume_for_reaction + float(oligo[7])
        volumes.append(oligo[7])
normalization_coefficient_min = round(1.0 / float(min(volumes)), 5)
normalization_coefficient = number_of_reactions
normalization_coefficient_relative = round(
    number_of_reactions / normalization_coefficient_min, 5
)
for oligo in oligos_table:
    if oligo[8] != "Vnorm, ul":
        oligo[8] = float(oligo[8]) * normalization_coefficient
        total_volume_for_mixing = total_volume_for_mixing + float(oligo[8])
for oligo in oligos_table:
    if oligo[8] != "Vnorm, ul":
        A260_afterSPE_exp = (
            A260_afterSPE_exp
            + float(oligo[5])
            * float(oligo[3])
            * float(oligo[8])
            / elution_volume
            / 1000000
        )
result_scheme_file_name = "result_" + scheme_file_name
# writing TBIO calculation results to file
with open(result_scheme_file_name, "w") as final_scheme_file:
    final_scheme_file.write(
        "TBIO scheme calculated for "
        + str(reaction_volume)
        + " ul reaction volume"
        + " for "
        + str(int(number_of_reactions))
        + " reactions"
        + "\n"
    )
    for oligo in oligos_table:
        for i in range(0, len(oligo)):
            final_scheme_file.write(str(oligo[i]))
            final_scheme_file.write("\t")
            final_scheme_file.write("\n")
            final_scheme_file.write("\n")
            final_scheme_file.write(
                "Min Normalization coefficient for volumes ="
                + str(normalization_coefficient_min)
                + "\n"
            )
        final_scheme_file.write(
            "Relative normalization coefficient for volumes for "
            + str(int(number_of_reactions))
            + " reactions = "
            + str(normalization_coefficient_relative)
            + "\n"
        )
        final_scheme_file.write(
            "Total volume for reaction = "
            + str(total_volume_for_reaction)
            + "ul"
            + "\n"
        )
        final_scheme_file.write(
            "Total volume for mixing = " + str(total_volume_for_mixing) + "ul" + "\n"
        )
        final_scheme_file.write(
            "A260 (1 cm) after SPE with "
            + str(int(elution_volume))
            + " ul elution = "
            + str(round(A260_afterSPE_exp, 3))
            + "\n"
        )
        # output to screen
for oligo in oligos_table:
    print(str(oligo) + "\n")
print("\t")
print(
    "Min Normalization coefficient for volumes = "
    + str(normalization_coefficient_min)
    + "\n"
)
print(
    "Relative normalization coefficient for volumes for "
    + str(int(number_of_reactions))
    + " reactions = "
    + str(normalization_coefficient_relative)
    + "\n"
)
print("Total volume for reaction = " + str(total_volume_for_reaction) + " ul" + "\n")
print("Total volume for mixing = " + str(total_volume_for_mixing) + " ul" + "\n")
print(
    "A260 (1 cm) after SPE with 750 ul elution = "
    + str(round(A260_afterSPE_exp, 3))
    + "\n"
)
