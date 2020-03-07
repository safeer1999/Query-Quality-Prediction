from whoosh.qparser import QueryParser
from whoosh import index

ix = index.open_dir('indexdir')

qp = QueryParser("content", schema=ix.schema)
q = qp.parse('The aspect below fails to compile with 1.1b2, producing the compilation error: -------------------- $ ajc com/ibm/amc/*.java com/ibm/amc/ejb/*.java d:/eclipse/runtime-workspace-ajsamples/Mock EJBs/com/ibm/amc/DemoBeanEJB.java:1: Cannot assign a value to the final field com.ibm.amc.DemoBean.ajc$interField$co m_ibm_amc$verbose !! no source information available !! 1 error --------------------------- package com.ibm.amc; import com.ibm.amc.ejb.SessionBean; /** * @author colyer * * To change this generated comment edit the template variable "typecomment": * Window&gt;Preferences&gt;Java&gt;Templates. * To enable and disable the creation of type comments go to * Window&gt;Preferences&gt;Java&gt;Code Generation. */ public aspect DemoBeanEJB { declare parents: DemoBean implements SessionBean; // THIS NEXT LINE IS THE CULPRIT static final boolean DemoBean.verbose = true; private transient String DemoBean.ctx; public void DemoBean.ejbActivate( ) { if ( verbose ) { System.out.println( "ejbActivate Called" ); } } } ------------------- Making the inter-type declaration non-final solves the problem...')

# from whoosh.analysis import SimpleAnalyzer,RegexTokenizer
# ana = RegexTokenizer(r'([a-zA-Z_\.0-9()]+)')
# print([token.text for token in ana('The aspect below fails to compile with 1.1b2, producing the compilation error: -------------------- $ ajc com/ibm/amc/*.java com/ibm/amc/ejb/*.java d:/eclipse/runtime-workspace-ajsamples/Mock EJBs/com/ibm/amc/DemoBeanEJB.java:1: Cannot assign a value to the final field com.ibm.amc.DemoBean.ajc$interField$co m_ibm_amc$verbose !! no source information available !! 1 error --------------------------- package com.ibm.amc; import com.ibm.amc.ejb.SessionBean; /** * @author colyer * * To change this generated comment edit the template variable "typecomment": * Window&gt;Preferences&gt;Java&gt;Templates. * To enable and disable the creation of type comments go to * Window&gt;Preferences&gt;Java&gt;Code Generation. */ public aspect DemoBeanEJB { declare parents: DemoBean implements SessionBean; // THIS NEXT LINE IS THE CULPRIT static final boolean DemoBean.verbose = true; private transient String DemoBean.ctx; public void DemoBean.ejbActivate( ) { if ( verbose ) { System.out.println( "ejbActivate Called" ); } } } ------------------- Making the inter-type declaration non-final solves the problem...')])

with ix.searcher() as s:
	results = s.search(q,limit=20)
	for i in results :
		print(i)

