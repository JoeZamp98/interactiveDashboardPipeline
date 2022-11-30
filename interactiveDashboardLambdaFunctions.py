import re

def map_offer_status(row):

    #DESCRIPTION: Determines if an individual respondent has or has not applied to a given employer, based on the response given in the column "E1 - Engagement" for general questions (ELSE segment), and based on the response given for an individual employer for employer-specific questions (IF/REGEX statement)

    #Local variables

    regex = "E[1-5].*"

    offer_status_correlations = {
    "E1" : "E1 - Engagement",
    "E2" : "E2 - Engagement", 
    "E3" : "E3 - Engagement",
    "E4" : "E4 - Engagement",
    "E5" : "E5 - Engagement"
    }

    status_column = "E1 - Engagement"

    #Function execution

    #If the variable name features an employer code, return applicant status for that particular employer
    if re.match(regex, row['allQuestions']):

        for employerCode in offer_status_correlations:

            corresponding_column = offer_status_correlations[employerCode]

            if (employerCode in row['allQuestions']) and ("Applied" in row[corresponding_column]):

                return "Applicant"

            elif(employerCode in row['allQuestions']) and ("Interviewed" in row[corresponding_column]):

                return "Applicant"

            elif (employerCode in row['allQuestions']) and ("Offer Stage" in row[corresponding_column]):

                return "Applicant" 

            elif (employerCode in row['allQuestions']) and ("Considered Company" in row[corresponding_column]):

                return "Non-Applicant"

            elif (employerCode in row['allQuestions']) and ("Never Considered" in row[corresponding_column]):

                return "Non-Applicant"
    
    #All other cases (non employer-specific questions) return applicant status for the primary employer/member
    else: 

        if ("Applied" in str(row[status_column])):

            return "Applicant"

        elif ("Interviewed" in str(row[status_column])):

            return "Applicant"

        elif ("Offer Stage" in str(row[status_column])):

            return "Applicant"

        elif ("Considered Company" in str(row[status_column])):

            return "Non-Applicant"

        elif ("Never Considered" in str(row[status_column])):

            return "Non-Applicant"

def map_offer_status_detailed(row):

    #DESCRIPTION: Determines if an individual respondent has or has not applied to a given employer, based on the response given in the column "E1 - Engagement" for general questions (ELSE segment), and based on the response given for an individual employer for employer-specific questions (IF/REGEX statement).  This version of the function has increased granularity in the returned status group compared to the baseline map_offer_status() function.  

    #Local variables

    regex = "E[1-5].*"

    offer_status_correlations = {
    "E1" : "E1 - Engagement",
    "E2" : "E2 - Engagement", 
    "E3" : "E3 - Engagement",
    "E4" : "E4 - Engagement",
    "E5" : "E5 - Engagement"
    }

    status_column = "E1 - Engagement"

    #Function execution

    #If the variable name features an employer code, return applicant status for that particular employer
    if re.match(regex, row['allQuestions']):

        for employerCode in offer_status_correlations:

            corresponding_column = offer_status_correlations[employerCode]

            if (employerCode in row['allQuestions']) and ("Applied" in row[corresponding_column]):

                return "Applicant"

            elif(employerCode in row['allQuestions']) and ("Interviewed" in row[corresponding_column]):

                return "Interviewed+"

            elif (employerCode in row['allQuestions']) and ("Offer Stage" in row[corresponding_column]):

                return "Interviewed+" 

            elif (employerCode in row['allQuestions']) and ("Considered Company" in row[corresponding_column]):

                return "Non-Applicant"

            elif (employerCode in row['allQuestions']) and ("Never Considered" in row[corresponding_column]):

                return "Non-Applicant"
    
    #All other cases (non employer-specific questions) return applicant status for the primary employer/member
    else: 

        if ("Applied" in str(row[status_column])):

            return "Applicant"

        elif ("Interviewed" in str(row[status_column])):

            return "Interviewed+"

        elif ("Offer Stage" in str(row[status_column])):

            return "Interviewed+"

        elif ("Considered Company" in str(row[status_column])):

            return "Non-Applicant"

        elif ("Never Considered" in str(row[status_column])):

            return "Non-Applicant"
        
def convert_employer_coding(row):

    # DESCRIPTION: Based on the employer code ('E1', 'E2', etc.), returns the appropriate respective employer name

    employer_code = ''

    if 'E1' in row['allQuestions']:

        employer_code = row['Employer1']
    
    elif 'E2' in row['allQuestions']:

        employer_code = row['Employer2']
    
    elif 'E3' in row['allQuestions']: 

        employer_code = row['Employer3']
    
    elif 'E4' in row['allQuestions']:

        employer_code = row['Employer4']

    elif 'E5' in row['allQuestions']:

        employer_code = row['Employer5']

    emp_name = employer_code

    return emp_name

def determine_desirability(row, member_desirability_dict):

    #DEFINITION: Searches for the member name in the member_desirability_dict (defined in generate_deep_dives() function), returns the appropriate value

    desirability_value = member_desirability_dict.get(row)

    return str(desirability_value)

def determine_rank(row, member_rank_dict):

    #DEFINITION: Searches for the member name in the member_rank_dict (defined in the generate_deep_dives() function), returns the appropriate value

    rank_value = member_rank_dict.get(row)

    return str(rank_value)

def determine_member_benchmark(row):

    #DEFINITION: Based on employer code, determines whether a given response belongs to the member or benchmark group.  All E2-E5 responses, even if they are secondary responses from the primary employer, are pushed into the benchmark.  

    classification = ''

    if 'E1' in row['allQuestions']:

        classification = 'Member'
    
    elif 'E2' in row['allQuestions']:

        classification = 'Benchmark'
    
    elif 'E3' in row['allQuestions']: 

        classification = 'Benchmark'
    
    elif 'E4' in row['allQuestions']:

        classification = 'Benchmark'

    elif 'E5' in row['allQuestions']:

        classification = 'Benchmark'

    return classification

def force_rank_conversion(row):

    #DEFINITION: Generates a new column that houses company names instead of question coding (i.e. ProspectPosition_1) where appropriate.  Applied in Deep Dives - Force Rank aggregation.  

    associated_employer = ''
    original_item = row['allQuestions']

    if 'ProspectPosition_1' in row['allQuestions']:

        associated_employer = row['Employer1']

        return associated_employer

    elif 'ProspectPosition_2' in row['allQuestions']:

        associated_employer = row['Employer2']

        return associated_employer

    elif 'ProspectPosition_3' in row['allQuestions']:

        associated_employer = row['Employer3']

        return associated_employer

    elif 'ProspectPosition_4' in row['allQuestions']:

        associated_employer = row['Employer4']

        return associated_employer

    elif 'ProspectPosition_5' in row['allQuestions']:

        associated_employer = row['Employer5']

        return associated_employer

    else: 

        return original_item
