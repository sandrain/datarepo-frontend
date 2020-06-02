from enum import Enum

class Record():
    """ Class representing an OSTI IAD2 Record

        id	                    The unique identifier for the record (used for updates on submission)
        accession_number	    The unique designation for the user's own reference to this content
        title	                A name or title by which the record is known
        authors	                Contains a listing of person(s) responsible for the content, as object references.
        site_code	            The site code assigned to the user account for grouping content.
        description	            A short description or abstract
        publisher	            The name of the entity that holds, archives, distributes, releases, or produces the resource
        country	                The country in which this version of the record was published
        publication_date	    The publication date
        date_record_added	    The date the record was added
        date_record_updated	    The date the record was last updated
        date_first_registered	The date the DOI was first minted, if present
        date_last_registered	The date the DOI was last updated, if present
        doi	                    The Digital Object Identifier (DOI)
        doi_infix	            Optional infix value used for unique DOI construction
        site_url	            The URL containing the record content, which the DOI will redirect to
        product_type	        The product type; usually one of "Dataset", "Text", or "Collection"
        product_type_specific	A short description of the record content type, or type of data
        keywords	            A listing of broad topics applying to the data or its subject matter
        language	            The primary language of the resource
        availability	        If applicable, the office or organization to refer access requests to
        research_organization	If credited, the organization name that performed the research
        sponsoring_organization	If credited, the organzation name that sponsored / funded the research
        contributors	        Contains a listing of persons or organizations that contributed to the content
        related_identifiers	    Contains a listing of related identifiers; usually DOIs or URLs related to the content in some specified manner
        report_numbers	        The report number associated with the entry
        contract_numbers	    Any contract or funding numbers associated with this record
        other_numbers	        Any additional identifying numbers associated with this record
        doi_message	            If present, the error condition of the last failed DOI submission
    """
    def __init__(self):
        self.id = None

class Author():
    """
        Class representing an Author / Contributor

        first_name	        A person's first, or given, name
        middle_name	        A person's middle name or initial, if present
        last_name	        A person's last, or family, name
        full_name	        For organizations, the listed name or description of the organization
        orcid	            The ORCID of this author/contributor, if any
        email	            A contact email address
        affiliations	    Contains a listing of any affiliations for this author/contributor
        contributor_type	(Contributors only)The type of contribution made by this contributor
    """

class RelatedIdentifier():
    """
        Class representing related Identifiers

        identifier_value	The DOI or URL value of the related identifier
        identifier_type	    One of "DOI" or "URL" to identify the type of content
        relation_type	    One of the recognized relation types description this identifier's relation to the record
    """

class RelationshipTypes(Enum):
    """
    Codes used to define inter- and intra-work relationships between this record (A) and another record (B). Often there are reciprocal relationships between A and B defined separately by each work.
    
    IsCitedBy	        Indicates A is listed as a citation by B.
    Cites	            Indicates A lists B as a citation.
    IsSupplementTo	    Indicates A is a supplemental work to B.
    IsSupplementedBy	Indicates B is a supplement to A.
    IsContinuedBy	    Indicates A is continued by B.
    Continues	        Indicates A is a continuation of B.
    Describes	        Indicates that A describes B.
    IsDescribedBy	    Indicates that A is described by B.
    HasMetadata	        Indicates B has metadata about A.
    IsMetadataFor	    Indicates A contains the metadata for B.
    HasVersion	        Indicates B has a version of A.
    IsVersionOf	        Indicates A is a version of B.
    IsNewVersionOf  	Indicates A is a newer version of B.
    IsPreviousVersionOf	Indicates B is a newer version of A.
    IsPartOf	        Indicates A is a portion of B, as in a series.
    HasPart	            Indicates A includes the part B, for series or containers.
    IsReferencedBy	    Indicates A is referenced by B.
    References	        Indicates A references B.
    IsDocumentedBy	    Indicates B contains documentation about A. (e.g., software documentation, user manual)
    Documents	        Indicates A is the documentation for B.
    IsCompiledBy	    Indicates B is used to compile or create A.
    Compiles	        Indicates B is result of compilation or creation of A.
    IsVariantFormOf	    Indicates A is a variation or different version of B.
    IsOriginalFormOf	Indicates A is the original version of B.
    IsIdenticalTo	    Indicates A and B are identical.
    IsReviewedBy	    Indicates B contains review information of A.
    Reviews	            Indicates A contains a review of B.
    IsDerivedFrom	    Indicates B is the source on which A is based.
    IsSourceOf	        Indicates A is the source on which B is based.
    IsRequiredBy	    Indicates A is required by B.
    Requires	        Indicates A requires B.
    Obsoletes	        Indicates A replaces or renders B obsolete.
    IsObsoletedBy	    Indicates A is replaced by or obsoleted by B.
    """

    IsCitedBy	        = 1
    Cites	            = 2
    IsSupplementTo	    = 3
    IsSupplementedBy	= 4   
    IsContinuedBy	    = 5
    Continues	        = 6
    Describes	        = 7
    IsDescribedBy	    = 8
    HasMetadata	        = 9
    IsMetadataFor	    = 10
    HasVersion	        = 11
    IsVersionOf	        = 12
    IsNewVersionOf  	= 13  
    IsPreviousVersionOf = 14
    IsPartOf	        = 15
    HasPart	            = 16
    IsReferencedBy	    = 17
    References	        = 18
    IsDocumentedBy	    = 19
    Documents	        = 20
    IsCompiledBy	    = 21
    Compiles	        = 22
    IsVariantFormOf	    = 23
    IsOriginalFormOf	= 24  
    IsIdenticalTo	    = 25
    IsReviewedBy	    = 26
    Reviews	            = 27
    IsDerivedFrom	    = 28
    IsSourceOf	        = 29
    IsRequiredBy	    = 30
    Requires	        = 31
    Obsoletes	        = 32
    IsObsoletedBy	    = 33

class IdentifierTypes():
    """
    Codes for supported types of identifier values for defining related identifiers.

    ARK	    Archival Resource Key; URL designed to support long-term access to information objects. In general, ARK syntax is of the form (brackets indicate [optional] elements: [http://NMA/]ark:/NAAN/Name[Qualifier]
    arXiv	arXiv identifier; arXiv.org is a repository of pre-prints of scientific papers in the fields of mathematics, physics, astronomy, computer science, quantitative biology, statistics, and quantitative finance.
    bibcode	Astrophysics Data System bibliographic codes; a standardized 19 character identifier according to the syntax yyyyjjjjjvvvvmppppa. See http://info-uri.info/registry/OAIHandler?verb=GetRecord&metadataPrefix=reg&identifier=info:bibcode/
    DOI	    Digital Object Identifier; a character string used to uniquely identify an object. A DOI name is divided into two parts, a prefix and a suffix, separated by a slash.
    EAN13	European Article Number, now renamed International Article Number,but retaining the original acronym, is a 13-digit barcoding standard which is a superset of the original 12-digit Universal Product Code (UPC) system.
    EISSN	Electronic International Standard Serial Number; ISSN used to identify periodicals in electronic form (eISSN or e-ISSN).
    Handle	A handle is an abstract reference to a resource.
    IGSN	International Geo Sample Number; a 9-digit alphanumeric code that uniquely identifies samples from our natural environment and related sampling features.
    ISBN	International Standard Book Number; a unique numeric book identifier. There are 2 formats: a 10-digit ISBN format and a 13-digit ISBN.
    ISSN	International Standard Serial Number; a unique 8-digit number used to identify a print or electronic periodical publication.
    ISTC	International Standard Text Code; a unique “number” assigned to a textual work. An ISTC consists of 16 numbers and/or letters.
    LISSN	The linking ISSN or ISSN-L enables collocation or linking among different media versions of a continuing resource.
    LSID	Life Science Identifiers; a unique identifier for data in the Life Science domain. Format: urn:lsid:authority:namespace:identifier:revision
    PMID	PubMed identifier; a unique number assigned to each PubMed record.
    PURL	Persistent Uniform Resource Locator.A PURL has three parts: (1) a protocol, (2) a resolver address, and (3) a name.
    UPC	    Universal Product Code is a barcode symbology used for tracking trade items in stores. Its most common form, the UPC-A, consists of 12 numerical digits.
    URL	    Uniform Resource Locator, also known as web address, is a specific character string that constitutes a reference to a resource. The syntax is:schema://domain:port/path?query_string#fragment_id
    URN	    Uniform Resource Name; is a unique and persistent identifier of an electronic document. The syntax is: urn:<NID<:<NSS> The leading urn:sequence is case-insensitive, <NID> is the namespace identifier, <NSS> is the namespace-specific string.
    w3id	Permanent identifier for Web applications. Mostly used to publish vocabularies and ontologies. The letters ‘w3’ stand for “World Wide Web”.
    """
