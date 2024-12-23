# --- Imports ------------------------------------------------------------------------ #

import contextlib
import csv
from io import TextIOWrapper

from tqdm import tqdm

from matzbiim.exceptions import SkipElement
from matzbiim.handlers import nysboe_handler
from matzbiim.utils import find_and_select_file

# --- Constants ---------------------------------------------------------------------- #

ORIGINAL_COLUMNS = [  #                 Original Name     Type        Description (Verbatim from Layout File)
    "last_name",  #                     LASTNAME          CHAR(50)    Last name.
    "first_name",  #                    FIRSTNAME         CHAR(50)    First name.
    "middle_name",  #                   MIDDLENAME        CHAR(50)    Middle name.
    "name_suffix",  #                   NAMESUFFIX        CHAR(10)    Name suffix, Jr: Sr, I, II,1,2, etc.
    "addr_number",  #                   RADDNUBMER        CHAR(10)    Residence House Number: Hyphenated numbers allowed.
    "addr_half_code",  #                RHALFCODE         CHAR(10)    Residence Fractional Address: 1/2, 1/3, etc.
    "addr_pre",  #                      RPREDIRECTION     CHAR(10)    Residence Pre-Street Direction (e.g. the “E” in 52 E Main St).
    "addr_street",  #                   RSTREETNAME       CHAR(70)    Residence Street Name.
    "addr_post",  #                     RPOSTDIRECTION    CHAR(10)    Residence Post Street Direction (e.g. the “SW” in 1200 Pecan Blvd SW).
    "addr_apt_type",  #                 RAPARTMENTTYPE    CHAR(10)    Residence Apartment / Unit Type (e.g. APT, UNIT, LOT, SUITE).
    "addr_apt",  #                      RAPARTMENT        CHAR(15)    Residence Apartment / Unit Number.
    "addr_nonstandard",  #              RADDRNONSTD       CHAR(250)   If Residential address is non standard format, the address will be filled in this field.
    "addr_city",  #                     RCITY             CHAR(50)    Residence City.
    "addr_zip",  #                      RZIP5             CHAR(5)     Residence Zip Code 5
    "addr_zip4",  #                     RZIP4             CHAR(4)     Zip code plus 4
    "mail_addr1",  #                    MAILADD1          CHAR(100)   Mailing Address 1 Free Form address
    "mail_addr2",  #                    MAILADD2          CHAR(100)   Mailing Address 2 Free Form address
    "mail_addr3",  #                    MAILADD3          CHAR(100)   Mailing Address 3 Free Form address
    "mail_addr4",  #                    MAILADD4          CHAR(100)   Mailing Address 4 Free Form address
    "date_of_birth",  #                 DOB               CHAR(8)     Date of Birth YYYYMMDD
    "gender",  #                        GENDER            CHAR(1)     Gender (Optional)
    "party",  #                         ENROLLMENT        CHAR(3)     Political Party Code
    "other_party",  #                   OTHERPARTY        CHAR(30)    Name of Party if Voter Checks “Other” on registration form
    "county_id",  #                     COUNTYCODE        INT(2)      County code 2 Digit County Code
    "election_district",  #             ED                INT(3)      Election district / Precinct Code
    "legislative_district",  #          LD                INT(3)      Legislative district
    "municipality",  #                  TOWNCITY          CHAR(30)    Town/City
    "ward",  #                          WARD              CHAR(3)     Ward
    "congressional_district_id",  #     CD                INT(3)      Congressional district
    "senate_district_id",  #            SD                INT(3)      Senate district
    "assembly_district_id",  #          AD                INT(3)      Assembly district
    "last_voted_date",  #               LASTVOTERDATE     CHAR(8)     Last date voted, YYYYMMDD
    "prev_year_voted",  #               PREVYEARVOTED     CHAR(4)     Last year voted (from registration form)
    "prev_county_voted",  #             PREVCOUNTY        CHAR(2)     Last county voted in (from registration form)
    "prev_address_voted",  #            PREVADDRESS       CHAR(100)   Last registered address
    "prev_name_voted",  #               PREVNAME          CHAR(150)   Last registered name (if different)
    "county_voter_id",  #               COUNTYVRNUMBER    CHAR(50)    County Voter Registration Number, Assigned by County
    "registration_date",  #             REGDATE           CHAR(8)     Application Date, YYYYMMDD (date application was received or postmarked)
    "id_required",  #                   IDREQUIRED        CHAR(1)     Identification Required Flag.
    "id_met",  #                        IDMET             CHAR(1)     Identification Verification Requirement Met Flag.
    "registration_source",  #           VRSOURCE          CHAR(10)    Application Source
    "registration_status",  #           STATUS            CHAR(10)    Voter Status Codes.
    "registration_status_reason",  #    REASONCODE        CHAR(15)    Status Reason Codes
    "inactive_date",  #                 INACT_DATE        CHAR(8)     Date Voter made ”Inactive”, YYYYMMDD
    "purge_date",  #                    PURGE_DATE        CHAR(8)     Date voter was “Purged”, YYYYMMDD
    "id",  #                            SBOEID            CHAR(50)    Unique NYS Voter ID
    "voter_history",  #                 VoterHistory      CHAR(1500)  Voting History separated by semicolons. Each voting history event is followed by voting method in parentheses.
]

# --- Subroutines -------------------------------------------------------------------- #


def count_rows(csv_file: TextIOWrapper) -> int | None:
    """

    This function counts the number of rows in the provided file.

    Paramaters
    ----------
    csv_file : TextIOWrapper
        The file to count the number of lines in.

    Returns
    -------
    int
        The number of rows in the file.
    None
        Returns None if an IOError is raised or if the user issues a KeyboardInterrupt.

    """

    with contextlib.suppress(KeyboardInterrupt, IOError):
        print(
            "Counting rows... (This will take a few minutes. Press C-c to continue without knowing the total number of rows.)"
        )

        return len(csv_file.readlines())

    return None


# --- Routines ----------------------------------------------------------------------- #


def csv_iterate(input_path: str) -> None:
    with (
        open(input_path, encoding="unicode_escape") as input_file,
        open("./data/output.csv", mode="w") as output_file,
    ):
        dialect = csv.Sniffer().sniff(input_file.read(1024))
        dialect.strict = True
        input_file.seek(0)

        row_count = count_rows(input_file)
        input_file.seek(0)

        csv_reader = csv.DictReader(
            input_file, fieldnames=ORIGINAL_COLUMNS, dialect=dialect
        )

        csv_writer = csv.DictWriter(
            output_file,
            fieldnames=ORIGINAL_COLUMNS,
            dialect=csv.get_dialect("excel"),
            strict=True,
        )

        csv_writer.writeheader()

        voters: tqdm[dict[str, str]] = tqdm(
            csv_reader,
            total=row_count,
            desc="Processing voters... ",
            unit=" voters",
            colour="green",
        )

        for voter in voters:
            try:
                for column, value in voter.items():
                    try:
                        voter[column] = nysboe_handler.handle(column, value)

                    except NotImplementedError:
                        continue

            except SkipElement:
                continue

            try:
                csv_writer.writerow(voter)

            except csv.Error:
                print("Writing row failed!\n\n" + str(voter))

            finally:
                del voter


def run() -> None:
    input_path = find_and_select_file("AllNYSVoters")

    if input_path is not None:
        csv_iterate(input_path)

    else:
        print("No file selected; exiting...")
        return


if __name__ == "__main__":
    run()
