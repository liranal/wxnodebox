from Vfs import *
from VfsSelection import *
from ProgressDlg import *
from OpCopy import *
from OpMove import *
from OpDelete import *

OP_COPY   = 1
OP_MOVE   = 2
OP_DELETE = 3
OP_MKDIR  = 4
OP_RENAME = 5


class OpManager:
    def __init__ (self):
        self.m_pDlg = None

    #void OnOperationDone(Op *pOp);
    def OnOperationDone(self, pOp):
        #ifdef __GNUWIN32__
        #destroy dialog
        self.m_pDlg.Show(False)
        self.m_pDlg.Destroy()
        #// delete m_pDlg;                   #// no need to do this
        #endif
        #//TOFIX mark as finished
        #//delete pOp;

    #Op *NewOperation(int nOp);
    def NewOperation(self, nOp):
        #TODO self.pOp?
        pOp = None

        #ifdef __GNUWIN32__
        #create dialog
        self.m_pDlg = CProgressDlg (NULL, 1, _("Operation in progress ..."), wxDefaultPosition, wxDefaultSize, wxCAPTION)
        self.m_pDlg.Show(True)
        #endif

        #create operation object on heap
        if (nOp == OP_COPY):
            pOp = OpCopy ()
        elif (nOp == OP_DELETE):
            pOp = OpDelete ()
        elif (nOp == OP_MOVE):
            pOp = OpMove ()

        return pOp

    #def StartOperation(int nOp, Vfs *pVfsSrc, Vfs *pVfsDst, VfsSelection &sel);
    def StartOperation(self, nOp, pVfsSrc, pVfsDst, sel):
        pOp = self.NewOperation (nOp)

        #TOFIX store Op pointer in some container (for multiple paralel operations)

        #start the operation
        if(pOp):
            #initialize
            pOp.m_pVfsSrc = pVfsSrc
            pOp.m_pVfsDst = pVfsDst
            pOp.m_objSrcItems = sel
            pOp.m_pManager = self
            #run
            pOp.RunOperation()

